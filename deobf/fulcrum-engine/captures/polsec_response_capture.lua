local g = type(getgenv) == "function" and getgenv() or _G
local marker = "Z,e=O(D[E](I(D,E+1,e))),E+A-1;"
local replacement = marker .. "if D[E+1]==3 then __ps_record(Z[1],D[E+2]) end;"
local prefix = [=[
local __ps_session
local function __ps_save_session(value)
    if type(value) == "number" or type(value) == "string" then
        __ps_session = value
    end
end
local function __ps_record(response, request)
    pcall(function()
        if type(response) ~= "table" then return end
        local body = response.e
        if type(body) ~= "table" or body.e ~= "Valid key" then return end
        local lines = {}
        local function add(name, value)
            local kind = type(value)
            if kind == "number" then
                lines[#lines + 1] = name .. "=" .. string.format("%.17g", value)
            elseif kind == "string" then
                lines[#lines + 1] = name .. "=" .. string.format("%q", value)
            elseif kind == "boolean" then
                lines[#lines + 1] = name .. "=" .. tostring(value)
            else
                lines[#lines + 1] = name .. "_type=" .. kind
            end
        end
        add("a", body.a)
        add("b", body.b)
        add("c", body.c)
        add("session", __ps_session)
        if type(request) == "table" and type(request.b) == "table" then
            add("request4", request.b[4])
            add("request5", request.b[5])
            add("request6", request.b[6])
        end
        writefile("polsec_vm_handshake.txt", table.concat(lines, "\n"))
        warn("[PolSec capture] saved polsec_vm_handshake.txt")
    end)
end
]=]
local function patch(src)
    if type(src) ~= "string" or not src:find("Luraph", 1, true) or not src:find(marker, 1, true) then
        return src
    end
    local out = {}
    local from = 1
    local count = 0
    while true do
        local first, last = src:find(marker, from, true)
        if not first then break end
        out[#out + 1] = src:sub(from, first - 1)
        out[#out + 1] = replacement
        from = last + 1
        count += 1
    end
    out[#out + 1] = src:sub(from)
    local instrumented = table.concat(out)
    local indexMarker = "q=D[e];e-=1;D[e]=D[e][q];"
    local indexReplacement = indexMarker .. "if q==\"session\" then __ps_save_session(D[e]) end;"
    local parts = {}
    local start = 1
    while true do
        local first, last = instrumented:find(indexMarker, start, true)
        if not first then break end
        parts[#parts + 1] = instrumented:sub(start, first - 1)
        parts[#parts + 1] = indexReplacement
        start = last + 1
    end
    parts[#parts + 1] = instrumented:sub(start)
    pcall(writefile, "polsec_response_source.lua", src)
    warn("[PolSec capture] saved source and instrumented " .. count .. " VM call sites")
    return prefix .. table.concat(parts)
end
local function wrap(original)
    return function(src, ...)
        local ok, result = pcall(patch, src)
        return original(ok and result or src, ...)
    end
end
local function arm(env)
    if type(env) ~= "table" or rawget(env, "__polsec_response_armed") then return end
    local old = env.loadstring
    if type(old) == "function" then
        rawset(env, "loadstring", wrap(old))
        rawset(env, "__polsec_response_armed", true)
    end
end
pcall(arm, g)
pcall(arm, _G)
pcall(arm, shared)
if type(getfenv) == "function" then pcall(arm, getfenv()) end
warn("[PolSec capture] armed; run your usual loader")
