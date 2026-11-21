-- WOAJ polsec sandbox prelude: network is mediated, responses are injected
-- by fulcrum.py after a real round-trip. WOAJ_RESPONSES is baked in above.
WOAJ_RESPONSES = WOAJ_RESPONSES or {}
local realprint = print
local realloadstring = loadstring
local capCount = 0
local genv = {}
local function wlog(s) realprint("WOAJ_LOG\t" .. s) end

local function hexenc(s)
	if type(s) ~= "string" then s = tostring(s) end
	local t = {}
	for i = 1, #s do t[i] = string.format("%02x", string.byte(s, i)) end
	return table.concat(t)
end

local function sanitize(s)
	return (tostring(s):gsub("[\t\n\r]", " "))
end

local function emit_fetch(method, url, headers, body)
	local hj = "-"
	if type(headers) == "table" then
		local parts = {}
		for k, v in pairs(headers) do parts[#parts + 1] = tostring(k) .. ":" .. tostring(v) end
		if #parts > 0 then hj = hexenc(table.concat(parts, "|")) end
	end
	local bb = "-"
	if type(body) == "string" and #body > 0 then bb = hexenc(body) end
	realprint("WOAJ_FETCH\t" .. sanitize(method) .. "\t" .. sanitize(url) .. "\t" .. hj .. "\t" .. bb)
end

local function lookup(url)
	local hit = WOAJ_RESPONSES[url]
	if hit then return hit end
	local cut = string.match(url, "^[^?]*")
	if cut and cut ~= url and WOAJ_RESPONSES[cut] then return WOAJ_RESPONSES[cut] end
	for k, v in pairs(WOAJ_RESPONSES) do
		if #k >= 20 and string.sub(url, 1, #k) == k then return v end
	end
	return nil
end

local FAKE_BODY = '{"error":"sandbox_no_real_response"}'
local function do_request(opts)
	opts = opts or {}
	local method = string.upper(tostring(opts.Method or opts.method or "GET"))
	local url = tostring(opts.Url or opts.url or "")
	local headers = opts.Headers or opts.headers
	local body = opts.Body or opts.body
	local hit = lookup(url)
	if hit then
		wlog("HTTP " .. method .. " " .. sanitize(url) .. " -> real response " .. tostring(hit.status))
		local st = tonumber(hit.status) or 200
		return {Success = st < 400, StatusCode = st, StatusMessage = "", Body = hit.body, Headers = {}}
	end
	if not (string.sub(url, 1, 7) == "http://" or string.sub(url, 1, 8) == "https://") then
		wlog("HTTP " .. method .. " non-http url, skipped: " .. sanitize(url))
		return {Success = false, StatusCode = 0, StatusMessage = "sandbox: non-http url", Body = "", Headers = {}}
	end
	emit_fetch(method, url, headers, body)
	wlog("HTTP " .. method .. " " .. sanitize(url) .. " -> not yet fetched (queued)")
	return {Success = true, StatusCode = 200, Body = FAKE_BODY, Headers = {}}
end

local function http_get(url)
	return do_request({Method = "GET", Url = url}).Body
end

local function json_decode(s)
	if type(s) ~= "string" then return nil end
	local pos = 1
	local n = #s
	local function skip()
		while pos <= n do
			local c = string.sub(s, pos, pos)
			if c == " " or c == "\t" or c == "\n" or c == "\r" then pos = pos + 1 else break end
		end
	end
	local parse
	parse = function()
		skip()
		local c = string.sub(s, pos, pos)
		if c == "{" then
			pos = pos + 1
			local obj = {}
			skip()
			if string.sub(s, pos, pos) == "}" then pos = pos + 1 return obj end
			while true do
				local k = parse()
				skip()
				if string.sub(s, pos, pos) ~= ":" then error("json: expected :") end
				pos = pos + 1
				obj[k] = parse()
				skip()
				local d = string.sub(s, pos, pos)
				if d == "," then pos = pos + 1
				elseif d == "}" then pos = pos + 1 return obj
				else error("json: bad object") end
			end
		elseif c == "[" then
			pos = pos + 1
			local arr = {}
			skip()
			if string.sub(s, pos, pos) == "]" then pos = pos + 1 return arr end
			while true do
				arr[#arr + 1] = parse()
				skip()
				local d = string.sub(s, pos, pos)
				if d == "," then pos = pos + 1
				elseif d == "]" then pos = pos + 1 return arr
				else error("json: bad array") end
			end
		elseif c == '"' then
			local out = {}
			pos = pos + 1
			while true do
				local ch = string.sub(s, pos, pos)
				if ch == "" then error("json: unterminated string") end
				if ch == '"' then pos = pos + 1 break end
				if ch == "\\" then
					local e = string.sub(s, pos + 1, pos + 1)
					pos = pos + 2
					if e == "n" then out[#out + 1] = "\n"
					elseif e == "t" then out[#out + 1] = "\t"
					elseif e == "r" then out[#out + 1] = "\r"
					elseif e == "b" then out[#out + 1] = "\b"
					elseif e == "f" then out[#out + 1] = "\f"
					elseif e == "u" then
						local hx = string.sub(s, pos, pos + 3)
						pos = pos + 4
						out[#out + 1] = string.char(tonumber(hx, 16) or 63)
					elseif e ~= "" then out[#out + 1] = e end
				else
					out[#out + 1] = ch
					pos = pos + 1
				end
			end
			return table.concat(out)
		elseif c == "t" then pos = pos + 4 return true
		elseif c == "f" then pos = pos + 5 return false
		elseif c == "n" then pos = pos + 4 return nil
		else
			local num = string.match(s, "^-?%d+%.?%d*[eE]?[+-]?%d*", pos)
			if num then pos = pos + #num return tonumber(num) end
			error("json: unexpected char " .. c)
		end
	end
	local ok, v = pcall(parse)
	if ok then return v end
	wlog("JSONDecode failed on " .. sanitize(string.sub(s, 1, 120)))
	return nil
end

local function enc(v, depth)
	depth = depth or 0
	local tv = type(v)
	if tv == "string" then return '"' .. v:gsub('[%c"\\]', function(c) return string.format("\\u%04x", string.byte(c)) end) .. '"'
	elseif tv == "number" then return tostring(v)
	elseif tv == "boolean" then return tostring(v)
	elseif tv == "table" then
		if depth > 6 then return "..." end
		local parts = {}
		local n = 0
		for k, val in pairs(v) do
			n = n + 1
			if n > 40 then parts[#parts + 1] = "...(" .. n .. ")" break end
			local kt = type(k)
			parts[#parts + 1] = (kt == "string" and '"' .. tostring(k) .. '":' or tostring(k) .. ":") .. enc(val, depth + 1)
		end
		return "{" .. table.concat(parts, ",") .. "}"
	end
	return tostring(v)
end

local function capture(src, chunkname)
	capCount = capCount + 1
	realprint("WOAJ_PAYLOAD_START\t#" .. capCount .. "\tsize=" .. #tostring(src) .. "\tname=" .. sanitize(chunkname))
	realprint(tostring(src))
	realprint("WOAJ_PAYLOAD_END")
	local f, e = realloadstring(tostring(src), tostring(chunkname))
	if not f then wlog("payload compile err " .. tostring(e)) return function() end end
	return function(...)
		local ok, err = pcall(f, ...)
		wlog("payload run ok=" .. tostring(ok) .. " err=" .. tostring(err))
	end
end
loadstring = function(src, cn) return capture(src, cn) end

local function stub(name)
	return setmetatable({}, {
		__index = function(t, k) local v = stub(name .. "." .. tostring(k)) rawset(t, k, v) return v end,
		__call = function(t, ...) local parts = {} for i = 1, math.min(select("#", ...), 3) do local v = select(i, ...) local tv = type(v) if tv == "string" then tv = "string:" .. v:sub(1, 60) elseif tv == "table" then tv = "table" else tv = tostring(v):sub(1, 30) end parts[i] = tv end wlog("CALL " .. name .. "(" .. table.concat(parts, ", ") .. ")") return stub(name .. "()") end,
		__tostring = function() return name end,
		__add = function() return 0 end, __sub = function() return 0 end,
		__mul = function() return 0 end, __div = function() return 0 end,
		__concat = function() return "" end, __len = function() return 0 end,
		__eq = function() return false end, __lt = function() return false end, __le = function() return false end,
		__newindex = function(t, k, v) rawset(t, k, v) end,
	})
end

local function makeservice(svcname)
	local st = stub("svc." .. svcname)
	rawset(st, "JSONEncode", function(self, v) local j = enc(v) realprint("WOAJ_JSON\t" .. j:sub(1, 8000)) return j end)
	rawset(st, "JSONDecode", function(self, v) return json_decode(v) end)
	rawset(st, "RequestAsync", function(self, opts) return do_request(opts) end)
	rawset(st, "GetAsync", function(self, url) return do_request({Method = "GET", Url = url}).Body end)
	rawset(st, "PostAsync", function(self, url, data, ct) return do_request({Method = "POST", Url = url, Body = data, Headers = {["Content-Type"] = tostring(ct or "application/x-www-form-urlencoded")}}).Body end)
	rawset(st, "HttpGet", function(self, url) return do_request({Method = "GET", Url = url}).Body end)
	rawset(st, "GenerateGUID", function() return "WOAJ-GUID" end)
	return st
end

local taskstub = setmetatable({}, {__index = function(t, k)
	if k == "spawn" or k == "defer" then return function(f, ...) if type(f) == "function" then local ok, e = pcall(f, ...) if not ok then wlog("SPAWNERR " .. tostring(e)) end return ok end wlog("task." .. tostring(k) .. " nonfunc " .. type(f)) return f end end
	if k == "wait" then return function(d) return 0 end end
	wlog("task." .. tostring(k)) return stub("task." .. tostring(k))
end})

local gamestub = setmetatable({}, {__index = function(t, k)
	if k == "IsLoaded" then return function() return true end end
	if k == "GetService" then return function(_, svc) return makeservice(tostring(svc)) end end
	if k == "HttpGet" or k == "HttpGetAsync" then return function(self, url) return do_request({Method = "GET", Url = url}).Body end end
	if k == "HttpPost" or k == "HttpPostAsync" then return function(self, url, data, ct) return do_request({Method = "POST", Url = url, Body = data, Headers = {["Content-Type"] = tostring(ct or "application/x-www-form-urlencoded")}}).Body end end
	local v = stub("game." .. tostring(k)) rawset(t, k, v) wlog("GET game." .. tostring(k)) return v
end})

game = gamestub
workspace = stub("workspace")
script = stub("script")
Instance = stub("Instance")
Enum = stub("Enum")
task = taskstub
request = do_request
http_request = do_request
syn = setmetatable({request = do_request}, {__index = function(t, k) return stub("syn." .. tostring(k)) end})
http = setmetatable({request = do_request, get = function(_, url) return http_get(url) end, post = function(_, url, data, ct) return do_request({Method = "POST", Url = url, Body = data, Headers = {["Content-Type"] = tostring(ct or "application/x-www-form-urlencoded")}}).Body end}, {__index = function(t, k) return stub("http." .. tostring(k)) end})
writefile = function(path, data)
	capCount = capCount + 1
	realprint("WOAJ_PAYLOAD_START\t#" .. capCount .. "\tsize=" .. #tostring(data) .. "\tname=writefile:" .. sanitize(path))
	realprint(tostring(data))
	realprint("WOAJ_PAYLOAD_END")
end
readfile = function(path) wlog("readfile " .. sanitize(path) .. " (empty)") return "" end
isfile = function() return false end
isfolder = function() return false end
listfiles = function() return {} end
getgenv = function() return genv end
getrenv = function() return getfenv() end
identifyexecutor = function() return "WOAJ Sandbox" end
_G = genv
wlog("prelude done")
