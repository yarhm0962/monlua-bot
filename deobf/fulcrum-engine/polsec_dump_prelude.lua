local realprint = print
local realloadstring = loadstring
local capCount = 0
local function wlog(s) realprint("WOAJ_LOG\t" .. s) end
local function capture(src, chunkname)
	capCount = capCount + 1
	realprint("WOAJ_PAYLOAD_START\t#" .. capCount .. "\tsize=" .. #tostring(src) .. "\tname=" .. tostring(chunkname))
	realprint(tostring(src))
	realprint("WOAJ_PAYLOAD_END")
	local f, e = realloadstring(tostring(src), tostring(cn or chunkname))
	if not f then wlog("payload compile err " .. tostring(e)) return function() end end
	return function(...)
		local ok, err = pcall(f, ...)
		wlog("payload run ok=" .. tostring(ok) .. " err=" .. tostring(err))
	end
end
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
local function makeservice(svcname)
	local st = stub("svc." .. svcname)
	rawset(st, "JSONEncode", function(self, v) local j = enc(v) realprint("WOAJ_JSON\t" .. j:sub(1, 4000)) return j end)
	rawset(st, "JSONDecode", function(self, v) wlog("JSONDecode " .. tostring(v):sub(1, 400)) return {} end)
	rawset(st, "RequestAsync", function(self, opts) realprint("WOAJ_REQ\t" .. enc(opts, 3):sub(1, 2500)) return {Success = true, StatusCode = 200, Body = '{"a":"1","b":"2"}'} end)
	rawset(st, "GetAsync", function(self, url) realprint("WOAJ_REQ\tGET " .. tostring(url)) return '{"a":"1","b":"2"}' end)
	return st
end
local taskstub = setmetatable({}, {__index = function(t, k)
	if k == "spawn" or k == "defer" then return function(f, ...) if type(f) == "function" then local ok, e = pcall(f, ...) if not ok then wlog("SPAWNERR " .. tostring(e)) end return ok end wlog("task." .. tostring(k) .. " nonfunc " .. type(f)) return f end end
	if k == "wait" then return function(d) return 0 end end
	wlog("task." .. tostring(k)) return stub("task." .. tostring(k))
end})
local gamestub = setmetatable({}, {__index = function(t, k)
	if k == "IsLoaded" then return function() return true end end
	if k == "GetService" then return function(_, svc) wlog("GetService " .. tostring(svc)) return makeservice(tostring(svc)) end end
	local v = stub("game." .. tostring(k)) rawset(t, k, v) wlog("GET game." .. tostring(k)) return v
end})
game = gamestub
workspace = stub("workspace")
script = stub("script")
Instance = stub("Instance")
Enum = stub("Instance")
task = taskstub
getgenv = function() return getfenv() end
wlog("prelude done")
