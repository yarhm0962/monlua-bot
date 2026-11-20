local function find_consts()
	local ok, c = pcall(function()
		return rawget(getgenv and getgenv() or _G, "consts")
	end)
	if ok and type(c) == "table" then
		return c, "getgenv"
	end
	local ok2, c2 = pcall(function()
		return rawget(_G, "consts")
	end)
	if ok2 and type(c2) == "table" then
		return c2, "_G"
	end
	local ok3, c3 = pcall(function()
		return consts
	end)
	if ok3 and type(c3) == "table" then
		return c3, "global"
	end
	return nil, "none"
end

local c, src = find_consts()
if not c then
	warn("[consts] not found - run this AFTER the PolSec loadstring, same executor session")
	return
end

local parts = {}
local n = 0
for i = 1, 600 do
	local v = c[i]
	if v ~= nil then
		n += 1
		parts[i] = tostring(v)
	end
end

writefile("consts_dump.txt", table.concat(parts, ","))
print("[consts] saved " .. n .. " entries (source: " .. src .. ") -> consts_dump.txt")
print("[consts] first 5: " .. tostring(c[1]) .. ", " .. tostring(c[2]) .. ", " .. tostring(c[3]) .. ", " .. tostring(c[4]) .. ", " .. tostring(c[5]))
