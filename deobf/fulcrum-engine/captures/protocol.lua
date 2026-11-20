local players = game:GetService("Players")
local local_player = players.LocalPlayer
local http_service = game:GetService("HttpService")
local request_fn = request or http_request

local API = {
	session = "https://api.polsec.net/loader/session/",
	socket_sfx = "?socket=1",
	http = "https://api.polsec.net/runtime/socket/http",
	heartbeat = "https://api.polsec.net/runtime/socket/heartbeat",
	diagnostic = "https://api.polsec.net/runtime/socket/diagnostic",
}

local Protocol = {}
Protocol.session_id = nil
Protocol.allocation = nil
Protocol.auth_sent = false
Protocol.alive = true

function Protocol.open_session(hwid, key)
	local ok, response = pcall(function()
		return request_fn({
			Method = "GET",
			Url = API.session .. hwid .. "/" .. key .. API.socket_sfx,
		})
	end)
	if not ok or not response or response.StatusCode ~= 200 then
		return nil
	end
	return http_service:JSONDecode(response.Body)
end

function Protocol.socket_post(payload)
	local body = http_service:JSONEncode(payload)
	local ok, response = pcall(function()
		return request_fn({
			Method = "POST",
			Url = API.http,
			Body = body,
			Headers = { ["Content-Type"] = "application/json" },
		})
	end)
	if not ok or not response then
		return nil
	end
	if response.StatusCode == 401 then
		return nil, response.Body
	end
	return http_service:JSONDecode(response.Body)
end

function Protocol.auth(hwid, key, session_a, session_b)
	if Protocol.auth_sent then
		return
	end
	Protocol.auth_sent = true
	local response, err = Protocol.socket_post({
		a = 0,
		b = 1,
		c = 0,
		d = 1,
		e = {
			a = hwid,
			b = key,
			c = tostring(session_a),
			d = tostring(session_b),
		},
	})
	if not response then
		if err == "1003" then
			AntiTamper.show_error("Invalid token", "")
			local_player:Kick("Invalid token")
		else
			warn("PolSec: unable to connect. Please execute again.")
		end
		Protocol.alive = false
	end
	Protocol.session_id = response
end

function Protocol.heartbeat(hwid)
	while Protocol.alive do
		pcall(function()
			request_fn({
				Method = "POST",
				Url = API.heartbeat,
				Body = http_service:JSONEncode({}),
				Headers = { ["Content-Type"] = "application/json" },
			})
		end)
		task.wait(10)
	end
	warn("PolSec: unable to recover this execution. Please execute again.")
end

function Protocol.diagnostic(payload)
	pcall(function()
		request_fn({
			Method = "POST",
			Url = API.diagnostic,
			Body = http_service:JSONEncode(payload or {}),
			Headers = { ["Content-Type"] = "application/json" },
		})
	end)
end

function Protocol.poll(session_a, session_b)
	return Protocol.socket_post({
		a = tostring(session_a),
		c = {},
		b = tostring(session_b),
	})
end

return Protocol
