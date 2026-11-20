local HWID = "955789dbe862b654"
local KEY = "75ebc5c71bc6f8c8"

local genv = getgenv and getgenv() or _G
if type(genv.script_key) == "string" and #genv.script_key > 0 then
	KEY = genv.script_key
end

local players = game:GetService("Players")
local http_service = game:GetService("HttpService")
local request_fn = request or http_request

if not request_fn then
	warn("[dumper] no request function in this executor")
	return
end

local LOADER_URL = "https://api.polsec.net/loader/" .. HWID .. "/" .. KEY
local SESSION_URL = "https://api.polsec.net/loader/session/" .. HWID .. "/" .. KEY .. "?socket=1"
local SOCKET_URL = "https://api.polsec.net/runtime/socket/http"
local HEARTBEAT_URL = "https://api.polsec.net/runtime/socket/heartbeat"
local DIAGNOSTIC_URL = "https://api.polsec.net/runtime/socket/diagnostic"

local RAW_FILE = "polsec_raw.txt"
local DUMP_FILE = "polsec_dump.lua"

local can_write = type(writefile) == "function"

local transcript = {}
local chunks = 0
local payload = {}

local function flush()
	if can_write then
		writefile(RAW_FILE, table.concat(transcript, "\n"))
	end
end

local function out(s)
	print("[dumper] " .. s)
	transcript[#transcript + 1] = s
end

local function describe(v, d)
	local tv = type(v)
	if tv ~= "table" then
		if tv == "string" then
			return string.format("%q", v)
		end
		return tostring(v)
	end
	if d > 5 then
		return "{...}"
	end
	local parts = {}
	for k, vv in pairs(v) do
		parts[#parts + 1] = tostring(k) .. "=" .. describe(vv, d + 1)
	end
	return "{" .. table.concat(parts, ",") .. "}"
end

local function code_of(r)
	if type(r) ~= "table" then
		return nil
	end
	return r.StatusCode or r.statuscode or r.code
end

local function body_of(r)
	if type(r) ~= "table" then
		return nil
	end
	return r.Body or r.body or r.Content
end

local function headers_of(r)
	if type(r) ~= "table" then
		return nil
	end
	return r.Headers or r.headers
end

local function log_resp(tag, r)
	out(tag .. " <<< " .. tostring(code_of(r)))
	local h = headers_of(r)
	if h then
		out(tag .. " headers: " .. describe(h, 1):sub(1, 500))
	end
	local b = body_of(r)
	if b then
		out(tag .. " body[" .. #tostring(b) .. "]: " .. tostring(b):sub(1, 300))
	end
	transcript[#transcript + 1] = tag .. " FULLBODY: " .. tostring(body_of(r))
end

local function http_get(url, tag)
	local ok, r = pcall(function()
		return request_fn({ Method = "GET", Url = url })
	end)
	if ok and r then
		out("GET " .. url)
		log_resp(tag or "GET", r)
		flush()
		return r
	end
	out("GET " .. url .. " ERROR " .. describe(r, 0))
	flush()
	return nil
end

local function http_post(url, body, tag)
	local ok, r = pcall(function()
		return request_fn({
			Method = "POST",
			Url = url,
			Body = body,
			Headers = { ["Content-Type"] = "application/json" },
		})
	end)
	if ok and r then
		out("POST " .. url)
		out(">>> " .. tostring(body):sub(1, 400))
		log_resp(tag or "POST", r)
		transcript[#transcript + 1] = "POST " .. url
		transcript[#transcript + 1] = ">>> " .. tostring(body)
		flush()
		return r
	end
	out("POST " .. url .. " ERROR " .. describe(r, 0))
	flush()
	return nil
end

local function save_chunk(code)
	chunks += 1
	payload[#payload + 1] = code
	if can_write then
		writefile(DUMP_FILE, table.concat(payload, "\n"))
		writefile("polsec_chunk_" .. string.format("%03d", chunks) .. ".lua", code)
	end
	out("CHUNK " .. chunks .. " SAVED (" .. #code .. " bytes)")
end

local function harvest(frame, depth)
	if type(frame) ~= "table" or depth > 5 then
		return
	end
	for _, v in pairs(frame) do
		if type(v) == "string" then
			local is_lua = #v > 200 and (v:find("%f[%w_]local%f[%W_]") or v:find("loadstring") or v:find("game") or v:find("Fulcrum"))
			local is_json_wrap = v:find("^%s*[%[{]")
			if is_lua and not is_json_wrap then
				save_chunk(v)
			end
		elseif type(v) == "table" then
			harvest(v, depth + 1)
		end
	end
end

local KILL_MARKERS = { "BANNED:", "SESSION_END:", "Invalid sessionId", "Invalid token", "Invalid key", "Session ended" }

local function is_kill(body)
	if type(body) ~= "string" then
		return nil
	end
	for _, m in ipairs(KILL_MARKERS) do
		if body:find(m, 1, true) then
			return m
		end
	end
	return nil
end

out("writefile: " .. tostring(can_write) .. " | executor: " .. (identifyexecutor and tostring(identifyexecutor()) or "unknown"))
out("flow: loader-preflight -> session -> auth -> poll")

local lres = http_get(LOADER_URL, "LOADER")
if not lres or code_of(lres) ~= 200 then
	out("STOPPED: loader preflight failed")
	return
end
out("loader preflight ok (" .. #tostring(body_of(lres)) .. " bytes), opening session")

local sres = http_get(SESSION_URL, "SESSION")
if not sres or code_of(sres) ~= 200 then
	http_post(DIAGNOSTIC_URL, http_service:JSONEncode({ hwid = HWID, status = "session_fail" }))
	out("STOPPED: session open failed")
	return
end

local sok, sess = pcall(function()
	return http_service:JSONDecode(body_of(sres))
end)
if not sok or type(sess) ~= "table" then
	out("STOPPED: session body not JSON: " .. tostring(body_of(sres)):sub(1, 200))
	return
end

local sa = tostring(sess.a)
local sb = tostring(sess.b)
out("session a=" .. sa .. " b=" .. sb)

local ares = http_post(SOCKET_URL, http_service:JSONEncode({
	a = 0,
	b = 1,
	c = 0,
	d = 1,
	e = { a = HWID, b = KEY, c = sa, d = sb },
}), "AUTH")
if not ares or code_of(ares) == 401 then
	out("STOPPED: auth rejected: " .. tostring(ares and body_of(ares)))
	return
end

local aok, adata = pcall(function()
	return http_service:JSONDecode(body_of(ares))
end)
if aok and adata ~= nil then
	out("auth data: " .. describe(adata, 0))
end

task.spawn(function()
	while true do
		pcall(function()
			http_post(HEARTBEAT_URL, http_service:JSONEncode({}))
		end)
		task.wait(10)
	end
end)

out("authenticated, polling for payload")

while true do
	local r = http_post(SOCKET_URL, http_service:JSONEncode({ a = sa, c = {}, b = sb }), "POLL")
	if not r then
		task.wait(2)
	else
		local bod = body_of(r)
		if code_of(r) == 401 then
			out("STOPPED: socket rejected: " .. tostring(bod))
			return
		end
		local kill = is_kill(bod)
		if kill then
			out("STOPPED: " .. kill)
			return
		end
		if bod and #bod > 2 then
			local ok2, data = pcall(function()
				return http_service:JSONDecode(bod)
			end)
			if ok2 and type(data) == "table" then
				out("frame: " .. describe(data, 0):sub(1, 400))
				harvest(data, 0)
			end
		end
	end
	task.wait(1)
end
