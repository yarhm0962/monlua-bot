local g = (type(getgenv) == "function" and getgenv()) or _G
if type(g) ~= "table" then
	g = _G
end

local saves = 0
local seen = {}

local function save_src(src, tag)
	if type(src) ~= "string" or #src < 32 then
		return
	end
	if seen[src] then
		return
	end
	seen[src] = true
	saves += 1
	local name = string.format("polsec_%s_%d.lua", tag or "cap", saves)
	local ok = pcall(writefile, name, src)
	if ok then
		warn("[cap] saved " .. name .. " (" .. #src .. " bytes)")
	else
		warn("[cap] write failed for " .. name)
		warn("[cap] first 200: " .. src:sub(1, 200))
	end
	pcall(function()
		g.__POLSEC_LAST = src
	end)
end

local function classify(src)
	if src:find("polsec%.net", 1, false) or src:find("Fulcrum %[-", 1, false) or src:find("%Fulcrum", 1, false) then
		return "fulcrum"
	end
	if src:find("Luraph", 1, false) then
		return "luraph"
	end
	if src:sub(1, 21) == "return setmetatable({" or src:sub(1, 13) == "return({cH=fu" then
		return "payload"
	end
	return "chunk"
end

local function wrap(old)
	if type(old) ~= "function" then
		return old
	end
	return function(src, ...)
		if type(src) == "string" and #src >= 32 then
			local okc, tag = pcall(classify, src)
			save_src(src, okc and tag or "cap")
		end
		return old(src, ...)
	end
end

local function env_list()
	local t = {}
	pcall(function()
		local e = getgenv()
		if type(e) == "table" then
			t[#t + 1] = e
		end
	end)
	if type(_G) == "table" then
		t[#t + 1] = _G
	end
	if type(shared) == "table" then
		t[#t + 1] = shared
	end
	return t
end

local function arm()
	for _, env in ipairs(env_list()) do
		pcall(function()
			if type(env.loadstring) == "function" and not env.__pc_ls_ref then
				env.__pc_ls_ref = env.loadstring
				env.loadstring = wrap(env.__pc_ls_ref)
			end
			if type(env.load) == "function" and not env.__pc_load_ref then
				env.__pc_load_ref = env.load
				env.load = wrap(env.__pc_load_ref)
			end
		end)
	end
	pcall(function()
		if type(loadstring) == "function" and not g.__pc_ls_ref then
			g.__pc_ls_ref = loadstring
		end
	end)
end

arm()

task.spawn(function()
	for _ = 1, 120 do
		task.wait(0.25)
		arm()
	end
end)

warn("[cap] armed - now run the PolSec loadstring")
warn("[cap] files: polsec_fulcrum_*.lua (loader), polsec_payload_*.lua / polsec_luraph_*.lua (real script)")
