local g = type(getgenv) == "function" and getgenv() or _G
local marker = "Z,e=O(D[E](I(D,E+1,e))),E+A-1;"
local replacement = marker .. "if D[E+1]==3 then __ps_record(Z[1],D[E+2]) end;"
local __ps_export_writer = writefile
local prefix = [=[
local __ps_env = type(getgenv) == "function" and getgenv() or _G
local __ps_write = type(__ps_env) == "table" and __ps_env.__ps_capture_export or nil
if type(__ps_write) ~= "function" then __ps_write = writefile end
pcall(function(...)
    local args=table.pack(...)
    local lines={"count="..tostring(args.n)}
    for i=1,args.n do
        local x=args[i]
        lines[#lines+1]="arg"..i.."_type="..type(x)
        if type(x)=="string" then lines[#lines+1]="arg"..i.."="..string.format("%q",x)
        elseif type(x)=="number" or type(x)=="boolean" then lines[#lines+1]="arg"..i.."="..tostring(x)
        elseif type(x)=="function" then
            local ok,source,line,name=pcall(debug.info,x,"sln")
            if ok then lines[#lines+1]="arg"..i.."_source="..string.format("%q",tostring(source));lines[#lines+1]="arg"..i.."_line="..tostring(line);lines[#lines+1]="arg"..i.."_name="..string.format("%q",tostring(name)) end
        elseif type(x)=="table" then
            local count=0
            for k,v in pairs(x) do
                count+=1
                if count<=60 then
                    local label=(type(k)=="string" or type(k)=="number") and tostring(k) or ("<"..type(k)..">")
                    if type(v)=="number" or type(v)=="boolean" then lines[#lines+1]="arg"..i.."["..label.."]="..tostring(v)
                    elseif type(v)=="string" and #v<=200 then lines[#lines+1]="arg"..i.."["..label.."]="..string.format("%q",v)
                    else lines[#lines+1]="arg"..i.."["..label.."]_type="..type(v) end
                end
            end
            lines[#lines+1]="arg"..i.."_entries="..count
        end
    end
    local key=args[1]
    if key~=nil then
        local ok,val=pcall(function() return getfenv()[key] end)
        if ok then
            lines[#lines+1]="env_value_type="..type(val)
            if type(val)=="number" or type(val)=="boolean" then lines[#lines+1]="env_value="..tostring(val)
            elseif type(val)=="string" then lines[#lines+1]="env_value="..string.format("%q",val) end
        end
    end
    __ps_write("polsec_loader_entry_details.txt",table.concat(lines,"\n"))
    warn("[PolSec capture] saved polsec_loader_entry_details.txt")
end, ...)
local __ps_session
local __ps_state_saved = false
local function __ps_capture_state(cells)
    if __ps_state_saved then return end
    pcall(function()
        if type(cells) ~= "table" or type(cells[2]) ~= "table" then return end
        local cell = cells[2]
        if cell[4] ~= 76 or type(cell[5]) ~= "table" then return end
        local root = cell[5]
        if type(root[77]) ~= "table" or #root[77] ~= 383 or root[76] ~= 13483 then return end
        local lines = {"length=" .. tostring(#root[77])}
        for i = 1, #root[77] do
            if type(root[77][i]) ~= "number" then return end
            lines[#lines + 1] = tostring(root[77][i])
        end
        __ps_write("polsec_live_state_new.txt", table.concat(lines, "\n"))
        __ps_state_saved = true
        warn("[PolSec capture] saved polsec_live_state_new.txt")
    end)
end
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
        __ps_write("polsec_live_handshake_new.txt", table.concat(lines, "\n"))
        warn("[PolSec capture] saved polsec_live_handshake_new.txt")
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
    local loops = {
        "while true do local C,ld=e[F];",
        "while true do local z=e[F];",
        "while true do local z,Y=e[F];",
    }
    for _, loop in ipairs(loops) do
        local parts, start = {}, 1
        while true do
            local first, last = instrumented:find(loop, start, true)
            if not first then break end
            parts[#parts + 1] = instrumented:sub(start, last)
            parts[#parts + 1] = "if F==142 then __ps_capture_state(G) end;"
            start = last + 1
        end
        parts[#parts + 1] = instrumented:sub(start)
        instrumented = table.concat(parts)
    end
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
    if type(env) ~= "table" then return end
    rawset(env, "__ps_capture_export", __ps_export_writer)
    if rawget(env, "__polsec_response_armed") then return end
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
