local function mkstub(name)
  local mt = {}
  mt.__index = function(self, k) return mkstub(name.."."..tostring(k)) end
  mt.__namecall = function(self, ...) return mkstub(name..":call") end
  mt.__call = function(self, ...) return mkstub(name.."()") end
  mt.__tostring = function() return "<stub "..name..">" end
  return setmetatable({}, mt)
end
local REAL = {}
for _,k in ipairs({"string","math","table","os","bit32","coroutine","debug","utf8","buffer"}) do REAL[k]=_G[k] end
for _,k in ipairs({"print","pcall","xpcall","pairs","ipairs","tostring","tonumber","type","typeof","setmetatable","getmetatable","rawset","rawget","rawequal","rawlen","select","unpack","table_unpack","loadstring","getfenv","setfenv","error","assert","next","require","newproxy","gcinfo","tick","warn"}) do REAL[k]=_G[k] end
local REALG = _G
local ENV = setmetatable({}, {
  __index = function(t,k)
    if REAL[k] ~= nil then return REAL[k] end
    if REALG[k] ~= nil then return REALG[k] end
    local s = mkstub("E."..tostring(k)); rawset(t,k,s); return s
  end,
  __newindex = function(t,k,v) rawset(t,k,v) end,
})
local __vcount={}
function __vtrace(id,L,u,e)
  local c=__vcount[id] or 0
  if c<30000 then __vcount[id]=c+1 print('VMTRACE\t'..id..'\t'..L..'\t'..u..'\t'..e) end
end
__bdone=false
