local POLSEC_HWID = "955789dbe862b654"
local POLSEC_KEY = "75ebc5c71bc6f8c8"
local POLSEC_TOKEN = POLSEC_HWID .. ":" .. POLSEC_KEY
local POLSEC_TOKEN_SHA256 = "2ab80ae141b17f8e8ec6266171048dbacc255535afb6c3b7e25180eaea6d1be1"

local API_DIAGNOSTIC = "https://api.polsec.net/runtime/socket/diagnostic"
local API_HEARTBEAT = "https://api.polsec.net/runtime/socket/heartbeat"
local API_HTTP_SOCKET = "https://api.polsec.net/runtime/socket/http"
local API_SESSION = "https://api.polsec.net/loader/session/" .. POLSEC_HWID .. "/" .. POLSEC_KEY .. "?socket=1"
local API_SOCKET_SUFFIX = "?socket=1"

local TAMPER_NOTICE = "Polsec is a Lua whitelisting service, and attempting to deobfuscate, reverse-engineer, or otherwise bypass its protections is against the service's Terms of Service. Continuing to do so could potentially get the owner or other involved parties in trouble, including account or service consequences. Stop attempting to deobfuscate or bypass Polsec and leave the protected code alone."

local local_player = game:GetService("Players").LocalPlayer
local http_service = game:GetService("HttpService")
local request_fn = request or http_request

local known_executors = {
	Delta = true,
	Velocity = true,
	Hydrogen = true,
}
local executor_name = identifyexecutor and identifyexecutor() or "Unknown"

local session_id = nil
local auth_sent = false
local inflight = {}
local pending = {}
local alive = true
local allocation = nil
local terminal_buffer = {}

local env = getfenv()
local string_lib = string
local char_fn = string.char

local env_proxy = setmetatable({}, {
	__index = function(_, key)
		return env[key]
	end,
	__newindex = function(_, key, value)
		env[key] = value
	end,
})

local function is_untampered()
	if getmetatable(_G) ~= nil then
		return false
	end
	if env.print ~= rawget(env, "print") and env.getfenv().print ~= print then
		return false
	end
	if type(getfenv()) ~= "table" then
		return false
	end
	if isnewcclosure and not isnewcclosure(request_fn) then
		return false
	end
	return true
end

local function tamper_response()
	print(TAMPER_NOTICE)
	while true do
		task.wait()
	end
end

local function sha256_matches()
	return POLSEC_TOKEN_SHA256 == sha256(POLSEC_TOKEN)
end

-- Opens a session. The ?socket=1 variant returns {a = session_id, b = ticket}
-- on success; the bare endpoint returns a fresh plain-text session number.
local function open_session()
	local ok, response = pcall(function()
		return request_fn({
			Method = "GET",
			Url = API_SESSION,
		})
	end)
	if not ok or not response or response.StatusCode ~= 200 then
		return nil
	end
	local decoded = http_service:JSONDecode(response.Body)
	if decoded.error or decoded.code ~= 200 then
		return nil
	end
	return decoded
end

local function http_socket_send(payload)
	local body = http_service:JSONEncode(payload)
	local ok, response = pcall(function()
		return request_fn({
			Method = "POST",
			Url = API_HTTP_SOCKET,
			Body = body,
			Headers = { ["Content-Type"] = "application/json" },
		})
	end)
	if not ok or not response then
		return nil
	end
	if response.StatusCode == 401 then
		return nil, 1003
	end
	local decoded = http_service:JSONDecode(response.Body)
	if decoded.error then
		return nil, decoded.code
	end
	return decoded.data
end

local function send_diagnostic()
	pcall(function()
		request_fn({
			Method = "POST",
			Url = API_DIAGNOSTIC,
			Body = http_service:JSONEncode({
				executor = executor_name,
				hwid = POLSEC_HWID,
			}),
			Headers = { ["Content-Type"] = "application/json" },
		})
	end)
end

local function heartbeat()
	while alive do
		local ok = pcall(function()
			request_fn({
				Method = "POST",
				Url = API_HEARTBEAT,
				Body = http_service:JSONEncode({
					session = session_id,
					hwid = POLSEC_HWID,
				}),
				Headers = { ["Content-Type"] = "application/json" },
			})
		end)
		if not ok then
			alive = false
			break
		end
		task.wait(10)
	end
	if alive then
		return
	end
	warn("PolSec: unable to recover this execution. Please execute again.")
	local_player:Kick("PolSec: unable to recover this execution. Please execute again.")
end

local function show_error(title, message)
	local core_gui = game:GetService("CoreGui")
	local prompt = core_gui:FindFirstChild("RobloxPromptGui")
	if not prompt then
		return
	end
	local overlay = prompt:FindFirstChild("promptOverlay")
	if not overlay then
		return
	end
	local frame = Instance.new("Frame")
	local title_frame = Instance.new("Frame")
	local error_frame = Instance.new("Frame")
	local error_title = Instance.new("TextLabel")
	local error_message = Instance.new("TextLabel")
	local message_area = Instance.new("Frame")
	title_frame.Name = "TitleFrame"
	error_frame.Name = "ErrorFrame"
	error_title.Name = "ErrorTitle"
	error_message.Name = "ErrorMessage"
	message_area.Name = "MessageArea"
	frame.Parent = overlay
	title_frame.Parent = frame
	error_frame.Parent = frame
	message_area.Parent = error_frame
	error_title.Parent = title_frame
	error_message.Parent = message_area
end

local function terminate_session(reason)
	if reason:sub(1, 7) == "BANNED:" then
		local ban_reason = reason:sub(8)
		show_error("Banned: ", ban_reason)
		local_player:Kick("Banned: " .. ban_reason)
		return
	end
	if reason:sub(1, 12) == "SESSION_END:" then
		alive = false
		return
	end
end

local function execute_chunk(code)
	local chunk, err = loadstring(code)
	if chunk then
		local ok, result = pcall(chunk)
		if not ok then
			writefile("dbg.txt", tostring(result))
		end
		return result
	end
	writefile("dbg.txt", tostring(err))
	return nil
end

-- Auth frame (captured verbatim from the client VM):
-- {"a":0,"b":1,"c":0,"d":1,"e":{"a":hwid,"b":key,"c":session_a,"d":session_b}}
local function auth(session_a, session_b)
	if auth_sent then
		return
	end
	auth_sent = true
	local response, err_code = http_socket_send({
		a = 0,
		b = 1,
		c = 0,
		d = 1,
		e = {
			a = POLSEC_HWID,
			b = POLSEC_KEY,
			c = tostring(session_a),
			d = tostring(session_b),
		},
	})
	if not response then
		if err_code == 1003 then
			show_error("Invalid token")
			local_player:Kick("Invalid token")
		else
			warn("PolSec: unable to connect. Please execute again.")
		end
		alive = false
		return
	end
	session_id = response.session
	allocation = response.allocation
	auth_sent = response.answered and true or false
	if not auth_sent then
		show_error("Invalid key")
		local_player:Kick("Invalid key")
		alive = false
		return
	end
end

local function terminal_loop()
	while alive do
		local data = http_socket_send({
			session = session_id,
			poll = true,
		})
		if data then
			local kind = data.type
			if kind == "allocation" then
				allocation = data.value
			elseif kind == "terminal" then
				table.insert(terminal_buffer, data.value)
				execute_chunk(data.value)
			elseif kind == "rejected" then
				terminate_session("BANNED:" .. tostring(data.value))
			elseif kind == "answered" then
				pending[data.id] = data.value
			elseif kind == "Invalid sessionId" or kind == "Invalid token" or kind == "Invalid key" then
				alive = false
				break
			end
		else
			task.wait(0.5)
		end
	end
end

local function main()
	if not is_untampered() then
		tamper_response()
		return
	end
	if not sha256_matches() then
		tamper_response()
		return
	end
	if not request_fn then
		warn("PolSec: unable to connect. Please execute again.")
		return
	end
	local session = open_session()
	if not session then
		send_diagnostic()
		warn("PolSec: unable to connect. Please execute again.")
		return
	end
	session_id = session
	task.spawn(heartbeat)
	auth(session and session.a, session and session.b)
	if not alive then
		return
	end
	terminal_loop()
end

main()
