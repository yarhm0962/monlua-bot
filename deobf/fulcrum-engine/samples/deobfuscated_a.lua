-- deobfuscated by discord.gg/printed
-- fulcrum polsec runtime | strings decrypted with the O/Q/U/V ciphers


f1 = getfenv
f8 = function(data, key, seed)
local length = #data

if length == 0 then
	return ""
end
local a, b, c, d, e = key[1], key[2], key[3], key[4], key[5]
local out = {}

for i = 1, length do
	seed = (seed * a + b) % 16777216
	local f = seed + (seed // 256) * d + (seed // 65536) * e
	out[i] = string.char(((data[i] - f) * c) % 256)
end
return table.concat(out)
end
f9 = function(data, key, seed)
local length = #data

if length == 0 then
	return ""
end
local a, b, c, d, e = key[1], key[2], key[3], key[4], key[5]
local out = {}

for i = 1, length do
	seed = (seed * a + b * a) % 16777216
	local f = seed + (seed // 256) * d + (seed // 65536) * e
	out[i] = string.char((data[i] * c - f) % 256)
end
return table.concat(out)
end
local length = #data

if length == 0 then
	return ""
end
local a, b, c, d, e = key[1], key[2], key[3], key[4], key[5]
local out = {}

for i = 1, length do
	seed = (seed * a + -b) % 16777216
	local f = seed + (seed // 256) * d + (seed // 65536) * e
	out[i] = string.char(((data[i] + f) * c) % 256)
end

do return table.concat(out) end
f10 = function(data, key, seed)
local length = #data

if length == 0 then
	return ""
end
local a, b, c, d, e = key[1], key[2], key[3], key[4], key[5]
local out = {}

for i = 1, length do
	seed = (seed * a + -b * a) % 16777216
	local f = seed + (seed // 256) * d + (seed // 65536) * e
	out[i] = string.char((data[i] * c + f) % 256)

do return table.concat(out) end
v1 = {2806325, 518223, 43, 255, 137}
v187 = {117, 122, 165, 28, 126}
v1 = {662981, 2767863, 95, 183, 189}
v187 = {245, 44}
v188 = {245, 44}
v188 = {159, 95, 54, 82, 224, 105, 212, 191}
v2 = {2825393, 1182141, 171, 239, 61}
v1 = {2825393, 1182141, 171, 239, 61}
v3 = {159, 95, 54, 82, 224, 105, 212, 191}
v3 = {20, 142, 40, 163, 108, 19, 127, 78, 123, 236, 153, 168, 33, 186, 211, 152, 180, 142, 32, 158, 42, 134, 105, 195, 211, 175, 253, 152, 172, 146, 208, 175, 27, 210, 186, 12, 135, 127, 241, 204, 78, 98, 129, 224, 246, 47, 123, 38, 87, 94, 79, 71, 126, 61, 131, 80, 74, 180, 6, 93, 199, 98, 23, 53}
v1 = {340661, 2847643, 55, 119, 39}
v3 = {41, 176, 235, 59, 76, 172, 114}
v1 = {1555645, 3966379, 147, 161, 189}
v4 = {3938021, 3283243, 69, 115, 111}
v1 = {}

while v5 do
v4 = {1298177, 2526807, 133, 129, 197}
v1 = {13, 213, 22, 35, 124, 100, 92}
v6 = {76, 76, 112, 12, 169, 44, 180, 18, 116, 92, 39, 119, 100, 201, 59, 72, 233, 115, 229, 31, 89, 22, 225, 8, 15, 61, 152, 84, 244, 66, 157, 124, 114, 192, 60, 99, 9, 152, 215, 31, 46, 101, 127, 95, 91, 27, 32, 47, 159, 73, 113, 62, 225, 204, 223, 163, 105, 125, 95, 107, 207, 234, 131, 18, 64, 206, 240, 168, 249, 96, 159, 131, 156, 114, 196, 207, 224, 130, 73, 148, 96, 140, 228, 180, 148, 18, 254, 220, 161, 248, 0, 98, 139, 116, 109, 56, 62, 101, 91, 189, 67, 242, 227, 231, 210, 145, 190, 10, 41, 95, 116, 61, 246, 57, 111, 96, 165, 20, 31, 84, 180, 118, 205, 99, 169, 41, 75, 227, 150, 151, 4, 26, 127, 178, 98, 74, 50, 240, 126, 185, 94, 21, 77, 176, 86, 188, 80, 81, 236, 95, 106, 151, 183, 170, 27, 241, 94, 46, 229, 134, 156, 127, 113, 48, 61, 139, 189, 13, 170, 123, 220, 195, 132, 68, 125, 146, 120, 247, 106, 216, 23, 136, 253, 191, 236, 197, 184, 92, 243, 228, 209, 115, 176, 171, 172, 75, 199, 52, 212, 2, 147, 49, 52, 180, 226, 66, 195, 100, 83, 82, 69, 173, 223, 240, 97, 18, 94, 255, 124, 146, 127, 50, 55, 147, 243, 200, 170, 68, 199, 119, 225, 83, 8, 126, 241, 46, 56, 33, 111, 209, 188, 61, 101, 96, 87, 42, 34, 68, 199, 2, 134, 104, 181, 8, 153, 25, 8, 93, 209, 17, 102, 136, 55, 48, 117, 242, 110, 142, 201, 132, 221, 141, 116, 1, 136, 55, 27, 155, 190, 1, 188, 97, 232, 88, 32, 217, 119, 77, 150, 93, 7, 186, 83, 224, 83, 82, 94, 110, 144, 121, 114, 123, 9, 216, 207, 172, 26, 121, 76, 64, 141, 117, 232, 237, 24, 50, 232, 95, 144, 216, 192, 111, 112, 62, 39, 243, 200, 83, 36, 92, 99, 82, 231, 101, 12, 194, 238, 182, 117, 35, 127, 50, 188, 226, 204, 248, 39, 252, 193, 114, 53, 66, 161, 246, 23, 206, 169, 90, 49, 238, 254, 136, 230, 218, 110, 90, 103, 241, 133, 7, 159, 253, 30, 56, 65, 63, 23, 32, 225, 77, 234, 246, 246, 184}
v4 = {790653, 835007, 21, 35, 197}
v6 = {252, 217, 2, 90}
v7 = {3189345, 435517, 153, 187, 75}
v7 = {1995225, 1763503, 209, 43, 169}
v8 = {228, 113, 84, 245, 116, 156}
v7 = {1866561, 3542541, 229, 193, 127}
v189 = {73, 88, 145, 29, 13}
v2 = {1866561, 3542541, 229, 193, 127}
v2 = {2524105, 2525395, 221, 131, 5}
v4 = {49, 130, 131, 98, 87, 92, 126, 28, 218, 70, 201, 255}
v9 = {2524105, 2525395, 221, 131, 5}
v4 = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
v9 = {1870621, 1612495, 101, 87, 73}

if v190==nil then
v9 = {3982485,2648187,125,9,187}
v4 = {186,3,254,211,98,214}

do
v191,v192 = 836529+v193,(v193-322)+(58151+322)
v3 = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
v2 = {1870621, 1612495, 101, 87, 73}
v8 = f1["getmetatable"]
v10 = f1["_G"]
v11 = (if v12==404587 then 1 else v13)(v10)
v14 = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
v15 = v10[(if v12==404587 then "Loaded" else v16)]
v9 = v194(v15)
v195 = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
v2 = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
v187 = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
v187 = "\10CA?J^"
v9 = {242, 62, 55, 250}
v189 = {856189, 665721, 31, 125, 215}
v17 = {242, 62, 55, 250}
f1[v196] = "trial"
v188 = {242, 62, 55, 250}
v11 = f1["game"]
v18 = v197("trial")

if true then
v14,v2,v19,v3 = v189,1,v2,""
else

do
v187 = "_''0&"
v8 = {216, 99, 43, 188}
v189 = {813493, 2363849, 91, 209, 183}
v17 = f1["getfenv"]
v10 = nil
v9 = (if v12==404587 then nil else v20)==(if v12==404587 then nil else v21)
v9 = {216, 99, 43, 188}
v9 = f1["getgenv"]
v187 = v9()
v187[v2] = nil
v22 = function(...)
t6 = {}

if (v198-v199)<=1476976 then

if 845345>(v198-v199) then

if 421578<(v198-v199) then

if not ((v198-v199)<555022) then

if (v198-v199)<650825 then

if (v198-v199)~=555023 then

if not ((v200-v199)~=84380) then

if 631730==631730 then

if v201==nil then
v2 = {54,116}
t1 = {1225369,32683,83,141,77}
end
v25,v26,v27 = 813493,v202,v25
else v28 = 631730
end
else if (v198-v199)>650825 then

if 674802<=(v198-v199) then

if not ((v198-v199)>=740313) then

if (v198-v199)~=674803 then

if not ((v200-v199)<=66027 or (v200-v199)>=66928) then

while false do
end

do
end
elseif not (1202~=(v200-v199)) then

do
end
elseif not (56552~=(v200-v199)) then
v14 = (if true then v29 else v30)[  v31 ]
v32 = (if false then v33 else true)[  "print" ]
v34 = v29 [(if true then nil else v35)]
v19,v36 = v32,f2(v37)
v14 = function(...)
local f11 = function(...)
t6 = {}
v203 = function(...)
v17 = "i u "

if v204==nil then
v205 = {2860197,1086565,159,65,161}
v22 = {84,65,(219-10)+10,224,162,158,64,(186-4)+4}
end
v206,v38,v39 = 160,nil,v38
v205 = {2466037, 1407571, 171, 73, 191}
v19 = {69, 42, 151, 35}

while false do
end
v22 = {204, 153, 207}
v205 = {2070789, 2721441, 119, 237, 211}
v40 = {79, 251, 6, 169, 61, 135}
;(if 536186~=536186 then t6 else v29)[(if v41 then t6 else v42)] = true
v202 = {2070789, 2721441, 119, 237, 211}

if 536186==536186 then

if v43 then

do
end
else v199 = v199+6786

do
end
end
else
end

while false do
end

while false do
end
v40 = #nil
v9 = {79, 251, 6, 169, 61, 135}
v44 = (if 536186==536186 then 0<v40 else v45)
v39 = (if 536186~=536186 then v46 else nil)
v15 = (if 536186~=536186 then v47 else nil)

while false do
end
v39 = (if 536186==536186 then v48 else v49)
v10 = {}

if false then
v17 = "!'4"
end

if false then
v22 = {84, 65, 219, 224, 162, 158, 64, 186}
v205 = {2860197, 1086565, 159, 65, 161}
end
v205 = {2883505, 2676723, 71, 49, 143}
v22 = {232, 124, 204, 197, 212, 141, 155, 148, 198, 23, 250, 75, 224, 52, 89, 105, 85, 35, 143, 24, 179, 123, 56, 45, 27, 59, 239, 40, 240, 71, 10, 16, 160, 94, 14, 59, 154, 135, 23, 147, 38, 57}
v14 = {79, 251, 6, 169, 61, 135}
v205 = {3419377, 393103, 51, 151, 1}
v22 = {122}
v205 = {1472245, 3161541, 25, 205, 41}

if false then
v205 = {2930117, 884187, 103, 35, 73}
end
v22 = {79, 251, 6, 169, 61, 135}

if false then
v206 = {}
end
v22 = v50[v207]

if 536186==536186 then
return
else
end
v3 = {231, 93, 152, 38}
v22 = {88, 18, 232, 210, 127}
v205 = {14313, 3952321, 55, 215, 231}

if false then
v205 = {1909437, 1929513, 27, 239, 71}
v22 = {189}
end

if 536186==536186 then
return
else
end

if false then
v39 = ":"
end
v27 = {122}
v51 = v208[  nil ]
v39 = v209(v43)
v39 = v29==401
v15 = {1472245, 3161541, 25, 205, 41}
v206 = {95}
v42 = {79, 251, 6, 169, 61, 135}
v44 = ""
v210 = {95}
v27 = (if 536186==536186 then "1003" else v52)
v42 = 12872556
v42 = nil>=v43

do
end
v206 = {14313, 3952321, 55, 215, 231}
v14 = ""
v22 = v50[nil]
v205 = v22[(if 536186~=536186 then v53 else nil)]
v42 = v205()
v51 = v9[v54]
v210 = (if 536186~=536186 then v55 else v206-nil)
v56 = v57~=0

if 1 then
v58,v27,v19,v59,v60,v205,v206 = 0,v60,nil,v61,401,nil,nil
else
v40,v27,v205,v210,v208,v14,v57,v10,v4,v42,v188,v1,v19,v206,v3,v6,v29,v2,v211,v22,v51,v58,v9,v61,v60,v43,v39,v17 = nil,0,v60,true,nil,v57,nil,nil,nil,v43,false,false,nil,nil,nil,v29,"°¸d®ÆIó",v61,v210,401,true,nil,nil,nil,v211,nil,"",false
end
v210 = nil>=60
v40 = 12872556
v29[v10] = nil
v27 = 1128
v6,v208,v60,v19,v211 = nil,nil,v211,nil,v60
v210 = (if 536186==536186 then v62 else v47)
v38 = {}
v15 = nil..""
v38[v1] = false
v1 = (if 536186~=536186 then t6 else "b")
v38[v1] = nil
v38[v1] = nil
v29,v10 = v27(nil,v60(v43,v38))
v3 = {242, 205, 246, 151, 253, 27, 188, 164}
v3 = {3, 156, 162, 136}
v210 = 12872556
v1 = {1633193, 1997593, 97, 67, 183}

do return end
v17 = "[HZ9"

if false then
v22 = {108, 246, 173, 111, 84}
v205 = {928453, 1054799, 79, 27, 129}
end
v39 = "[HZ9"
v22 = {1633193, 1997593, 97, 67, 183}
v17 = "[HZ9"
v188 = {3394941, 106039, 5, 65, 195}
v19 = {197, 197, 6, 67, 211}
v40 = ""

if false then
v19 = {141, 231, 43, 87}
v188 = {3127497, 1023777, 223, 193, 207}
end
v206 = {197, 197, 6, 67, 211}
v27[v210] = (if 536186~=536186 then t6 else v60)
v188 = (if 12872556~=v29 then true else not true)

if true then
v59,v39,v56,v42,v43,v14,v202,v61 = nil,true,v43,1,v19,nil,v61,nil
else

do
end
end

while false do
end
v39 = v50[nil]
v6 = (if 536186==536186 then v63 else v52)
v6 = (if 536186==536186 then 12872556 else t6)
;(if 536186==536186 then v60 else v64)[(if not v65 then t6 else v38)] = 1
v17 = 400<="pcall"
v3 = (if v59 then 536186~=536186 else 536186==536186)
v40 = (if 536186==536186 then v66 else t6)
v40 = "pcall"<v60
v202 = v57 [  v59 ]
v205 = {2856797, 2580771, 5, 57, 67}

if false then
v205 = {3645317, 3607153, 87, 69, 237}
end
return f11(v67,v212,v213,true,v214,v68,v69,v215,v70,v216,v71,v72,n14,v203,v217,1,v218,v219,v73,v220,v74,v75,nil,v192,v76,v221,n15,v211,v191,v222,v223,v77,...)
end

do
end
end
end
elseif (v200-v199)<84726 and 84396<(v200-v199) then
v78 = (nil) [  nil ]
v26 = v224(nil,5,v61)
v79 = {}
v79[v32] = false
v32,v78 = nil,false
v79[v32] = false
v32 = function(...)
local f12 = function(...)
t6 = {}
v215 = function(...)

do return v222 end
v210 = "6Vu"
v15 = {244, 180, 166}
v11 = (if 112633~=112633 then v81 else(378755+(-378750)))
v225 = (if v3==197 then true else not true)
v226 = {244, 180, 166}

if not v25 then

do
end
else

do
end
end

if 12872556 then
v29,v15,v8 = nil,3645317,nil
else
v222,v29,v221,v225,v57,v195,v61,v226,v15,v227,v82,v8 = v226,nil,197,nil,nil,v82,3645317,v57,v61,v225,true,nil
end
v228 = (if 112633==112633 then t6 else v83)
v228 = {}
v195 = {813493, 2363849, 91, 209, 183}

while false do
end

if false then
v210 = "bS!"
end
v10 = v228(v61)
v43[v59] = nil
v79 = ""
v225 = {244, 180, 166}
v84 = {813493, 2363849, 91, 209, 183}
v3 = getfenv[v229]
v15 = (if 112633~=112633 then t6 else v85)
v227 = v222[(if 112633==112633 then nil else v86)]
v87 = v59(nil)
v198,v200 = (if nil then v199+442638 else v199+442638),(if nil then(v199-827)+(24581+827) else v199+24024)
v15 = {251, 249, 101, 159, 170, 150, 136, 79}
v19 = {}

if false then
v15 = {35, 209, 32, 229, 131, 75, 205}
end

if false then
end

if false then
v15 = {195}
end
v79,v225,v87,v215,v230,v59,v221 = nil,v59,nil,v60,nil,nil,5618367
v40 = (1)[(if 112633~=112633 then v88 else true)]
v89 = v25 (1)
v230 = v89~="string"
v198,v200 = (if 14 then 478386+v199 else v199+478386),(if 14 then v199+19102 else(v199-898)+(30686+898))
v210 = "#F\9"

if false then
v202 = {}
end
v15 = ""

if false then
end

if false then
end
v8 = v231(nil,8)
v84 = {140, 218, 105, 110, 211, 155, 218, 168}

if 112633==112633 then

do
end
else
end
v1 = 112633==112633
v189 = {}
v54[v11] = (if true then nil else v90)

if 112633==112633 then
v43,v230,v3,v227,v61,v25,v60,v29,v221,v36,v87,v79,v84 = v61,nil,nil,nil,nil,v84,v43,nil,v60,v25,8,nil,v36
else
end

if not nil then

do
end
else

do
end
end
local v232,v233 = v61,nil
v6 = (if 112633~=112633 then v91 else v92)
v210 = {}
v210 = (if 112633==112633 then nil else t6)
v198,v200 = (v199-435)+(124139+435) ,  v199+96380
v202 = {112, 178, 92, 10, 88}
v202 = {162}

if not v36 then
v227,v36,v215,v79,n3,v8,v221,v84,v29 = nil,nil,true,v36,10323688,nil,v29,true,nil
else
v215,n3,v8,v221,v84,v29 = true,10323688,nil,v29,true,nil
end
v210 = ""

if nil then

do
end
else

do
end
end
v198,v200 = (if nil then(v199-698)+(124139+698) else v199+1656647),(if nil then 54736+v199 else 35384+v199)
v226 = ""
v210,v7,v6,v19,v215 = true,nil,1,1,true

if nil then
v189,v215,v222,v7,v195,v79 = nil,true,"Loaded",1,true,10323688
else
v1,v210,v189,v82,v215,v222,v225,v7,v195,v79 = true,nil,nil,nil,true,"Loaded",nil,1,true,10323688
end

if 112633==112633 then

do
end
else
end
v215 = v60(v59,true,8,nil,v61)
v198,v200 = (if nil then(v199-522)+(1644363+522) else 1644363+v199),(if nil then v199+92426 else(v199-162)+(46458+162))
v230 = (if 112633==112633 then v93 else v94)
v222 = (if nil then false else 112633==112633)

if nil then

do
end
else
v29,v79,v87,v10,v15,v40,v195,v1,v19,v43,v228,v59 = true,1,nil,true,nil,nil,true,1,v59,1,v29,v43
end
v228,v215 = "Loaded",1
;(if not v95 then v40 else t6)[(if not v95 then v87 else t6)] = 8
v202 = {208, 52, 103, 58, 179, 170, 241, 101}
v222 = ""
v225 = nil==5

if not v25 then

do
end
else

do
end
end
v189 = 1~=nil

if true then
v202,v225,v226 = nil,3834820,v202
else

do
end
end
v210 = "Banned: "

if false then
v15 = {146, 168, 166}
end
v230 = 1

if false then
end
v79 = 20~=""
v228 = not 1

if nil then

do
end
else
v202,v87,v227,v84,v195,v8,v54 = nil,nil,v54,nil,nil,1,nil
end

if false then
v15 = {251, 249, 101, 159, 170, 150, 136, 79}
end

if false then
end

if false then
v15 = {35, 209, 32, 229, 131, 75, 205}
end

if false then
end

if false then
v15 = {195}
end
v10 = true>=1
v198,v200 = (if 5 then 850310+v199 else(v199-763)+(850310+763)),(if 5 then(v199-288)+(21357+288) else(v199-497)+(20686+497))
v198,v200 = (if 1 then v199+850310 else(v199-96)+(1900942+96)),(if 1 then 30925+v199 else 60860+v199)

do
v228 = ""
end

if v234==nil then
v79 = {160, 46, 177, 50, 39, 178}
end

if v234==nil then
end

while false do
end
v79 = {186}

if 112633==112633 then

if false then
end

do
end
else
end
v79 = v226[  v60 ]
return f12(v67,v212,v213,nil,v214,v68,v69,nil,nil,v70,v216,v71,v72,n14,v203,v217,nil,v218,v219,v73,v220,v74,v75,nil,v192,v76,true,n15,v188,v211,v191,14,v223,v77,...)
end
v32 = (if false then v96 else v97["tonumber"])

do
end
end
end
else
v2 = {55}
t1 = {974173, 3252123, 169, 45, 79}
t1 = {3022485, 1647287, 17, 55, 81}
v2 = {212, 185, 152, 221}
v2 = {45, 170, 255, 254, 103, 228, 203, 87}
t1 = {3957681, 3608887, 159, 63, 15}
v38[v98] = nil
;(if not false then v38 else v99)[(if v100==631730 then v98 else v101)] = nil
v29,v102 = v44(v193,v103,nil)

while false do
end
v38 = {}

while false do
end
v103 = ","
v79 = nil +v29
v104 = string.char
v235 = {139, 155, 11, 5}
t1 = {858733, 396331, 57, 57, 153}
v235 = {65, 42, 141, 166, 232}
t1 = {1638753, 1237989, 205, 31, 167}
v105 = (if 0<s1 then true else false)
v32 = v106 <1

if nil then

do
end
else

do
end
end
v8 = "_qpp"
v34 = {114, 235, 118, 227, 156}
t1 = {3732981, 2995079, 187, 41, 169}
v34 = {142, 47, 32, 7, 159, 61, 105, 123}
t1 = {3146713, 2336353, 133, 139, 239}
v27 = {65, 42, 141, 166, 232}
v17 = "B#%$"

if false then
t1 = {587349,2251005,55,29,181}
v103 = {196}
end

do
v105 = 1
v17 = "B#%$"

while false do
v1 = {142, 53, 253, 76, 23, 75, 33, 178, 71, 190}
t1 = {1149329, 1663475, 177, 85, 39}

if 240753>(v198-v199) then

if (v198-v199)<=66184 then

if not ((v198-v199)>44093) then

if (v198-v199)~=44094 then

if 18884==(v200-v199) then
v78 = v34(nil)
v38 = nil==1
v8,v235,v193 = v235,v193,500
end
end
else if 66184<=(v198-v199) then

if not ((v200-v199)<=4816 or (v200-v199)>=5365) then

if 0 then

do
v2 = 1
end
else v199 = (v199+4637)
v26,v2,v235,v38,v25,v8,v230,v27 = nil,nil,nil,500,v235,nil,true,nil
end
elseif not ((v200-v199)~=44162) then

do
end
end
end
end
else if 134304>(v198-v199) then

if (v198-v199)~=109227 then

if 42227==(v200-v199) then
v103,v26,v230,v202,v8,v187 = "",true,true,nil,nil,v103
elseif 8769==(v200-v199) then
v202 = (if true then 1 else v107)
v38 = {}
v38[v98] = nil
v202,v103 = v103,true
elseif not ((v200-v199)>=35726)and 35443<(v200-v199) then

while false do
end
v38[v98] = true
v1,v230 = "",v1
end
end
else if (v198-v199)<236055 then

if (v198-v199)~=134305 then

if (v200-v199)==12696 then

if not "" then

do
end
else v199 = 7899+v199

do
v38 = 1
end
end
elseif 97932==(v200-v199) then
return
end
end
else if (v198-v199)>=236055 then

if (v200-v199)==83446 then
v202,v2 = (-777860+777861),(-452850+452853)
v98,v27 = (-879071+879072),true

do
end
elseif 89743>(v200-v199)and (v200-v199)>89540 then
v230,v202,v25,v235 = v25,v235,v103,true
end end end end end else if not ((v198-v199)>343171) then if 343171<=(v198-v199) then if not (98060~=(v200-v199)) then v1 = v52 ("",nil)
v19 = getfenv[v236]
return
end
else if 69183>(v200-v199)and (v200-v199)>68835 then

if v237==nil then
end

do
end
elseif (v200-v199)==23363 then

if false then
v17 = {(123+4)-4,231,(65+21)-21,0,(200+4)-4}
t1 = {3927629,2637093,153,69,229}
end
v193,v230 = "",v193
elseif not ((v200-v199)~=16013) then

if false then
end
v8,v25 = v25,500
elseif not (69725~=(v200-v199)) then

if v238==nil then
t1 = {2786549,1343509,189,151,235}
v17 = {232,184,51,136,195,(64+24)-24,115,174}
end

do
end
end
end
else if not ((v198-v199)<=347017) then

if not ((v198-v199)>=413044) then

if not ((v198-v199)<372293) then

if not (68673<=(v200-v199)or 67868>=(v200-v199)) then
f3 = function(...)
local f13 = function(...)
t6 = {}

if v239==nil then
end
n15,v61 = v61,nil

if v240==nil then
end

do
end
v188 = {79, 251, 6, 169, 61, 135}

if not false then

do
end
else

do
end
end
v11 = {79, 251, 6, 169, 61, 135}

if false then
end

while false do
end

while false do
end
v108 = v59[v57]
v14 = (if string~=740418 then v109 else 1879032)(v59,v61,7)
v110 = (if "Loaded"~=nil then false else string==740418)
v198,v200 = (v199-795)+(225804+795) ,  v199+84276
v14,v15,v4,n15,v189,v2,v241,v222,v59,v60,v61,v26 = v59 ,  v60 ,  v110 ,  1  ,  nil ,  v61 ,  nil  ,  65  ,  nil ,  nil ,  v57 ,  nil
v198,v200 = 1071870+v199  , (v199-967)+(96178+967)

while false do
end
v198,v200 = 917258+v199 ,  80865+v199
v203,v208,v227,v14,v214,v188,v189,v8,v211,v110,v108 = (if 1 then 65 else nil),(if 1 then nil else nil),(if 1 then nil else nil),(if 1 then nil else nil),(if 1 then true else true),(if 1 then 1 else 1),(if 1 then v110 else 1),(if 1 then 1 else 1),(if 1 then 1879032 else 1879032),(if 1 then 1 else v110),(if 1 then v59 else 1879032)
v198,v200 = (if 1 then(v199-114)+(1559664+114) else v199+1559664),(if 1 then(v199-273)+(97372+273) else 35624+v199)

while false do
end
v198,v200 = (if nil then 382036+v199 else(v199-344)+(382036+344)),(if nil then(v199-138)+(28191+138) else v199+15443)
local v242,v243 = nil,nil
v189 = v244(nil,nil,3)

if not false then
v6,v59,v11,v2,v54,v110,v195,v15,v227 = v110,nil,nil,nil,v245,nil,v54,nil,nil
else
v11,v15 = nil,nil
end

if false then
end

if false then
end

do return 8307615 end
local v246,v247 = nil,nil

if string==740418 then
v189 = v223 (nil,nil,3)

do
end
else
end

if not false then
v6,v59,v11,v2,v54,v110,v195,v15,v227 = v110,nil,nil,nil,v245,nil,v54,nil,nil
else

do
end
end

while false do
end

if true then
v245,v8,v17 = v54,"Invalid key",nil
else

do
end
end

do return false end
return f13(v67,v212,v213,v68,v69,nil,v216,v71,v72,nil,v217,nil,v218,v73,v220,v74,v75,nil,v192,v76,nil,nil,v191,nil,v223,...)
end
v44 = function(...)
local f14 = function(...)
t6 = {}

while false do
end
v3 = {79, 251, 6, 169, 61, 135}
v26 = "m%7_4X"
v248 = 1
v39 = {199, 243, 92}
v39 = {72}
v113 = {813493, 2363849, 91, 209, 183}
v1 = {146, 115, 229, 36, 94, 207, 121, 113, 95}
v39 = {79, 251, 6, 169, 61, 135}
v235 = {72}
v1 = {813493, 2363849, 91, 209, 183}
v228 = {146, 115, 229, 36, 94, 207, 121, 113, 95}
v18 = {251, 223, 74, 120}
v114 = {146, 115, 229, 36, 94, 207, 121, 113, 95}
v18 = {184, 130, 255, 242, 46, 206, 136}
v18 = {201, 202, 4, 10, 84, 73, 135, 41, 66, 186}
v14 = "9$&nN5"

while false do
end
v18 = {}
v18 = (if 349078==349078 then true else v115)
v188 = (if nil then not true else true)

if true then
v26,v15,v188,v9,v221,v217 = 3374953,v217,1,v18,1,nil
else
v26,v27,v223,v1,v116,v10,v235,v18,v9,v59,v19,v40,v2,v221,v39,v11,v3,v117,v208,v61,v113,v15 = 3374953,v217,1,true,1,v223,nil,nil,11680180,nil,v18,nil,v235,1,v60,v59,16310920,nil,nil,nil,nil,v61
end
v188[v235] = (if 349078==349078 then true else v118)
v235[v116] = (if 349078==349078 then nil else v81)
v116 = v249("","",1,1,v193,"request")
v235 = v119 [(if 349078==349078 then nil else v118)]
v117 = (if 349078==349078 then v114 else v120)[(if false then v115 else nil)]
local v250 = (if 349078~=349078 then t6 else nil)
v40 = v250(v114,v59,"ÌÚ")
v221 = (if 3374953=="ò6"then not false else 349078~=349078)
v15 = "L"
v1 = {72}
v208 = {72}
v40 = {72}
v8 = {146, 115, 229, 36, 94, 207, 121, 113, 95}
v44 = {162}
v235 = (if 349078~=349078 then v121 else v223)

while false do
end

if false then

do
end
else

do
end
end
v1 = "ò6"
v230 = {72}
v230 = v217[v211]
v221 = v230  [  v122 ]
v230 = "ÌÚ"
v1 = v217[v211]
;(if true then v228 else v123)[(if true then v59 else v81)] = nil
v228[v59] = nil
v2,v219 = v193(nil,v59,v223)
v235 = (if 349078~=349078 then v124 else not false)
v117 = not ""

if not 1 then

do
end
else

do
end
end
v9 = {153, 78, 173}

while false do
end

if v234==nil then
v18 = {130, 25, 72, 93, 171, 174}
end

if v234==nil then
end
v221 = v251(nil)
v125 = (if 349078==349078 then v223 else v20)

if not true then

do
end
else
v61,v10,v60,v19,v235,v223,v59,v40,v2,v39,v3,v188,v15 = "",false,true,v223,v59,nil,nil,nil,"",v60,12,nil,v61
end
v235 = v125[  t6  ]

if "" then

do
end
else

do
end
end

do
v11 = "ÌÚ"
end
v14 = {38, 246, 213}
v9 = {38, 246, 213}
v9 = {61, 205}
v1 = {93, 141, 62, 53, 234, 2, 73, 158, 90, 194, 0, 41, 89, 52, 94, 100, 145, 74, 36, 246, 163, 211, 178, 13, 6, 245, 74, 148, 234, 163, 202, 96, 39, 100, 217, 244, 229, 217, 37, 162, 234, 31, 247, 135, 94, 74, 41}
v1 = {183}

if false then
v39 = {20}
end
v9 = {186}
v18 = {183}

if 1 then
v228,v9,v230,v61,v223,v235,v2,v14 = "öÅ\\8\1ý",v230,v9,10067716,8237876,"gui",v223,"R2"
else

do
end
end
v3 = {186}
v1 = {27, 71, 107, 115}

if false then
end
v188,v14,v223,v15,v40 = nil,nil,"gui",v223,nil
v1 = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}

if false then
v1 = {76, 13, 194, 149, 225}
end
v9 = {186}
v18 = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}
v235 = "7"
v39 = {65, 213, 126, 179, 147, 217, 106, 119}
v9 = v252(nil,"gui")
v9 = getfenv[v253]

do
end
v208 = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}
v11 = {61, 205}
v2 = v125[nil]
v114 = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}

if not true then

do
end
else
v188,v60,v26,v18,v2,v221,v211,v10,v61,v15,v217,v14,v235,v3 = nil,nil,nil,1,nil,v217,v18,8237876,6309705,842907,v61,nil,nil,"gui"
end
v9 = 349078==349078
v2[v217] = nil
v39 = {100}
v39 = {219, 25, 99, 252, 137, 227, 118, 168, 47, 243, 82, 200}
v117 = {186}

if v248==nil then
v39 = {26, 115, 59, 121, 173, 90, 91, 158, 18, 171}
end

if 349078==349078 then
v3,v44,v188,v193,v38,v116,v39,v14,v219,v208,v40,v1,v2,v59 = true,6770358,842907,v39,v217,nil,nil,v219,nil,v193,1,842907,1,nil
else
end
v3 = {219, 25, 99, 252, 137, 227, 118, 168, 47, 243, 82, 200}
v39 = {186}
v114 = getfenv["warn"]
v8 = (if 349078==349078 then v114 else v126)(nil)
v9 = {186}
v114 = {}
v8 = v114[(if true then nil else t6)]
v39 = v254()
v9 = {186}
v10 = {61, 205}
v188 = {186}
v1 = {186}
v1 = (if nil>=9 then true else 349078~=349078)
v188 = "ÌÚ"

if not v193 then

do
end
else
v217,v223,v8,v27,v114 = nil,1,v223,nil,v217
end
v27 = v60(v211,"ò6")
v9 = {39, 107, 45, 78}
v9 = "ÌÚ"
v1 = {39, 107, 45, 78}

if 349078==349078 then

if v253==nil then
end

do
end
else
end
v235 = "G"
v39 = {195, 164, 76, 175, 34, 96, 178, 59}

while false do
end

do return end

while false do
end
v208 = "[l'J"
v26 = {195, 164, 76, 175, 34, 96, 178, 59}

if false then
end

if 349078==349078 then

if false then
end
v235,v114,v1,v59,v15,v10,v188 = nil,"authSent","SESSION_END:",12,10141998,1991552,nil
else
end
v9 = {39, 107, 45, 78}
v14 = "e\9NW4+Ag"

if false then
v39 = {10, 253}
end
v9 = {39, 107, 45, 78}
t2 = (if 349078==349078 then v61 else t6)[(if 349078==349078 then nil else v81)]
v228 = {}

while false do
end
v27 = "|B?|LY_("
v9 = {139, 68, 140, 13, 76, 243, 8, 70}

if 349078==349078 then

if false then
v14 = {(38+29)-29,(246-22)+22,213}
end
v211,v114,v27,v8,v44,v11,v9 = v9,nil,nil,10141998,1991552,"reported",1991552
else
end

if false then
end

while false do
end

if false then
v9 = {61, 205}
end

while false do
end

if false then
end

if false then
end
v40 = nil~="reported"
v114 = not 8387390

if 1 then
v193,v11,v8,v2 = "reported",nil,nil,"Y"
else
v188,v1,v193,v11,v8,v19,v117,v2 = 10141998,v59,"reported",nil,"math",nil,8387390,"Y"
end

if v255==nil then
v228 = "?e"
end
v230,v40,v25,v10,v188,v219,v26,v59,v14 = 15201458,"math",v219,v59,v25,"a",v211,10067716,9

if not false then
v39,v1,v3,v40,v228,v188,v10,v217 = 15201458,15201458,1991552,"request",10067716,"math",v217,nil
else

do
end
end
v39 = {}

while false do
end

if false then
v18 = {251, 223, 74, 120}
end

if false then
end

if false then
v18 = {184, 130, 255, 242, 46, 206, 136}
end

if false then
v228 = "- r\\"
end
v18 = {201, 202, 4, 10, 84, 73, 135, 41, 66, 186}

if v193 then

do
end
else

do
end
end
v117 = {}
;(if 349078~=349078 then v127 else v117)[(if true then v11 else v86)] = 1
;(if not false then v117 else v128)[(if 349078~=349078 then v129 else v11)] = 16310920
;(if not false then v117 else v130)[(if false then v131 else v11)] = 400
v235 = (if 349078==349078 then "Invalid sessionId" else t6)
v117[v11] = nil
v11 = {}
v235 = (if 349078~=349078 then v128 else "³\2\24Ne&")
t2 = v114[  nil  ]

do return 1 end

if false then
end

if false then
v188 = "JSONEncode"
end

if false then
end
t2 = (if 349078~=349078 then v128 else false)

if not true then

do
end
else

do
end
end
v18 = {}
t2 = (if 349078==349078 then t6 else v128)
v18[v40] = (if 349078==349078 then nil else v132)
v19[v40] = 504
t2 = {}
t2[v8] = true
v3 = (if 349078==349078 then nil else v133)
;(if 349078~=349078 then v119 else t2)[(if 349078~=349078 then t6 else v8)] = true

if true then

do
end
else
v25,v114,v193,v1,v38,v44,v223,v211,v3,v230 = "a",nil,7010719,v211,v25,nil,false,v193,nil,true
end
v14 = {}
v11 = (if 349078~=349078 then v134 else "a")
v14[v230] = nil

do return {} end
v228 = (if 349078~=349078 then v135 else t6)
v188 = (if 349078~=349078 then v136 else v93)
v11 = not 7010719

do return nil end
return f14(v67,v212,v213,v68,v69,8,v70,v216,v71,v72,nil,v217,true,v218,v73,v220,v74,v75,nil,v192,v76,3645317,nil,v191,nil,v223,...)
end
local f13 = function(...)
t6 = {}

while false do
end
v4 = {811333, 2798249, 15, 19, 69}
v22 = {209, 23, 211, 88, 184}
v4 = {3900049, 2279877, 133, 117, 179}
v22 = {239, 173}
v22 = {37, 89, 38, 133, 161, 200}
v4 = {510601, 2269061, 61, 47, 247}
v138 = {65, 40, 126, 121, 117, 237, 86, 76}
v138 = {173, 41, 108, 28}
v138 = {178, 208, 22, 189}
v139 = {2236017, 3494159, 159, 181, 155}
v187 = {178, 208, 22, 189}
v139 = {2916621, 1158297, 221, 145, 245}
v187 = {142, 21, 46, 1, 212, 220, 140, 63, 56, 92, 26, 105, 6, 11, 177, 8, 211, 108, 17, 209, 6, 204, 126, 11, 80, 174, 107, 224, 48, 182, 123, 72, 40, 173, 159, 9, 152, 137, 211, 12, 116, 31}
v139 = {685281, 788389, 69, 25, 59}
v187 = {20}
v139 = {754021, 1725939, 121, 149, 179}
v187 = {233, 30, 2, 60, 8}
v222 = {3535237, 488535, 27, 227, 15}
v187 = {129, 94, 41, 158}

while false do
end
v187 = {113, 200, 4, 254}
v222 = {2059717, 2965217, 187, 187, 167}
v187 = {81, 123, 250, 222, 110, 252, 69, 196}
v222 = {3124417, 838319, 207, 119, 63}
v222 = {2757085, 290473, 249, 227, 219}
v187 = {88, 98, 198, 110, 194, 132, 141}

while false do
end

if v234==nil then
v187 = {10, 254, 113, 158, 23, 191}
end
v222 = {2757085, 290473, 249, 227, 219}
v210 = {88, 98, 198, 110, 194, 132, 141}

if v234==nil then
end
v222 = {1190213, 1999771, 87, 125, 121}
v210 = {75, 27}

if v256==nil then
v222 = {39753,3419475,161,41,123}
v210 = {226,30,115,243}
end

do
end
v140 = v141[nil]
v214 = v140~=1

while false do
end
v142 = (if 1 then false else 291982==291982)

if not v142 then

do
end
else

do
end
end
v188 = (if v143~=1901 then 291982==291982 else false)

if not nil then
v11,v18,v57,v2,v3,v210 = nil,true,nil,true,nil,nil
else
v57,v2 = nil,true
end
v143 = (if false then v144 else getfenv["table"])
v222 = v231(nil,v145)
v139 = {}

do return v215(nil,nil,nil,v145,nil) end

do return nil end
v2 = v257("ò6")
v10 = {}
v146 = nil=="string"

if ",\"d\":" then

do
end
else

do
end
end
v11 = {2757085, 290473, 249, 227, 219}
v214 = v258(v141)
v222 = "table"~=nil

if true then
v18,v2,v25,v188,v187 = v191,true,nil,nil,9199125
else v199 = 491+v199
v193,v214,v2,v25,v188,v18,v187 = v191,v193,true,nil,nil,nil,9199125
end

if false then
end
v7 = {225, 77, 183, 43, 234, 169, 145, 195, 4, 77}
v10 = {225, 77, 183, 43, 234, 169, 145, 195, 4, 77}

while false do
end
v138 = 3645317
v22 = {2698125, 1152795, 107, 143, 147}
v22 = {654257, 3805441, 117, 127, 129}
v10 = {110, 82, 107, 234}

if false then
v10 = {1075977,2287171,103,99,55}
v18 = {87,(246-13)+13,75}
end
v147,v193,v187,v215,v139,v214 = nil,nil,v193,nil,v25,v60
v148 = getfenv["math"]
v187 = v148[  v57 ]
v139 = nil*v193
v22 = 0.75+nil
v139 = {110, 82, 107, 234}
v188 = 1~=nil
v150 = v259(v14)
v11 = {1142405, 3783405, 225, 71, 97}
v138 = {244, 204, 224}
v187 = {1142405, 3783405, 225, 71, 97}
v138 = {16}
v187 = {2132813, 3994521, 181, 163, 155}

if false then
end
v11 = {3285885, 1633817, 229, 127, 113}
v138 = {153, 254, 250, 94, 104, 30, 77, 247}
v4 = {2132813, 3994521, 181, 163, 155}
v18 = {110, 82, 107, 234}

if false then
v138 = {20, 236, 120}
v11 = {1400513, 1706043, 165, 143, 65}
end
v139 = {110, 82, 107, 234}

while false do
end
v15 = (nil) [  nil ]
v14 = v36+nil
v145[v151] = nil

while false do
end
v7 = {412197, 3748527, 213, 183, 181}
v3 = getfenv["rejected"]
v7 = v44[  nil ]
v22 = v3(v7)

while false do
end
v138 = {3285885, 1633817, 229, 127, 113}
v143 = getfenv["ý\5ú Z"]
t6 = {}
v152 = string
v18 = {813493, 2363849, 91, 209, 183}
v14 = {79, 251, 6, 169, 61, 135}
v227 = {3847741, 2836119, 31, 79, 115}
v187 = {3847741, 2836119, 31, 79, 115}
v18 = {36, 134, 100, 62, 146, 55, 106, 134, 215, 52}
return v153(nil,nil)

end
v3,v141 = v143(v191)

do
end

if not 1 then

do
end
else
v214,v187 = v187,true
end
v147 = {249, 11, 148, 179, 186, 215, 172}
v22 = {}
v139 = {3285885, 1633817, 229, 127, 113}
v2 = {3285885, 1633817, 229, 127, 113}

do return s3(nil,nil,nil,nil,nil,v29,nil) end

do
end
v210 = 404~=v154
v10 = v154==400
v188 = {618797, 2349785, 241, 135, 221}
v18 = {188}
s3[v155] = true
v210 = {}
v150 = (if nil==1 then true else not true)
v146 = v141 [  nil ]
v210 = {}

if not v191 then
v10,v210,v2,v191,v187,v7,v4,v18 = nil,v193,v191,nil,500,nil,1,nil
else

do
end
end

do return nil, true end
v18 = {194}
v7 = {2675657, 3109663, 165, 131, 179}
v7 = {1812189, 1988369, 189, 191, 25}
v18 = {192, 157, 7, 24, 84, 49, 96}

if not nil then

do
end
else
v205,v214 = 500,nil
end

do return v11(nil,nil,nil,nil,nil,v29,nil) end
v188 = 3645317
v222 = {262161, 1054369, 191, 33, 79}
v7 = {249, 88, 205, 44, 164, 50, 16, 92, 173}
v22 = 3645317

if false then
v214 = {2082453, 3775569, 87, 127, 181}
v7 = {253, 217, 65, 84}
end
s3 = 3645317

if true then

do
v3 = 3645317
end
else v199 = (v199+6301)
v4,v138,v147,v7,v3,n14,v2 = true,v193,false,true,n14,1,nil
end

while false do
end
;(if v156==291982 then s3 else v157)[(if v156==291982 then v155 else t6)] = true
v150 = getfenv["os"]
v155 = v150[  "clock" ]
v27 = v155()

if not true then
v215,v214,v18,v205 = v191,nil,nil,1990816
else

do
end
end

while false do
end

do return v158("reconnect",nil,0,nil,nil,v29,nil) end

if not nil then

do
end
else

do
end
end

if v260==nil then
end

do
end
v11 = {2097425, 1458709, 17, 231, 41}
v18 = {89}
v11 = {468909, 164045, 143, 57, 19}
v18 = {139, 159, 73, 149}
v2 = {262161, 1054369, 191, 33, 79}

do return nil, "clock" end
v11 = {262161, 1054369, 191, 33, 79}
v2 = {468909, 164045, 143, 57, 19}

do return v148(v57,nil,nil,nil,nil,v29,nil) end
v155 = (nil) [  nil ]

while false do
end

do return true, "http" end
v187 = {468909, 164045, 143, 57, 19}
v18 = {93, 107, 104, 105, 196}
v188 = {2073325, 1643977, 171, 219, 73}

while false do
end
v18 = {44}
v222 = {1678869, 3662927, 111, 217, 217}

if false then
v18 = {217}
v222 = {2854257, 2169051, 87, 113, 155}
end
v214 = {57, 142, 145, 235, 13, 211}
v188 = {1626705, 1702811, 115, 219, 19}
v147 = v154~=401

if true then
v146,v193,v205,v2,v3,v139,v60,v191,v187 = v187,nil,nil,9274641,v60,v214,1,v2,v191
else

do
end
end
v147 = "1003"~=3847741

do return v4(v191,nil,nil,nil,nil,v29,nil) end
v11 = {44}
v138 = {1678869, 3662927, 111, 217, 217}
v147 = {468909, 164045, 143, 57, 19}
;(if v156==291982 then v17 else v159)[(if v104 then v154 else v160)] = 3847741
v17[v154] = nil
;(if false then v161 else v17)[(if false then v162 else v154)] = nil
v17 = getfenv["os"]
v38 = (146) [(if false then t6 else "clock")]
v27 = {468909, 164045, 143, 57, 19}
v38 = (if nil then false else 291982==291982)
v14 = v17()
v44 = (nil) [  "JSONEncode" ]
v139 = {}
v2 = nil..""
;(if v156==291982 then v139 else v163)[(if not false then v141 else t6)] = "reconnect"
v139[v141] = nil
v139[v141] = nil
v17 = v44(nil,v139)
v154[v38] = nil
v44 = {}
v147 = {44}
v3 = {}
s3 = ",\"d\":".. nil
v155 = 152096 .. nil
v154,v38 = v44("https://api.polsec.net/runtime/socket/http","1003",v29)
v205 = {44}

if true then
v210,v139,v22,v60,v10,v25,v138,n14,v191,v188,v187,v57,v214,v222,v27,v4,v7,v11,v2,v3,v18,v43 = "b",-2,v57,nil,v138,v191,"terminal",1,152096,v205,",\"d\":",v214,",\"d\":",152096,n14,v193,"answered",v60,nil,"}",v25,152096
else
v22,v188,v11,v187,v27 = "terminal",",\"d\":",152096,"answered","}"
end
v7 = {}
v147[n14] = true
v143 = #"inflight"
v7 = {}

if false then
v11 = {3649009, 1959353, 231, 233, 217}
end
return f13(v67,v212,v213,nil,v68,v69,152096,v70,v216,v71,v72,nil,v217,true,v218,v73,v220,v74,v75,nil,v192,v76,3645317,nil,v191,152096,v223,...)
end

if true then
v230,v187,v1,v38 = 152096,"inflight","",nil
else v199 = (v199+5381)
v32,v230,v193,v187,v2,v1,v38 = 2,v193,152096,"inflight",nil,"",nil
end
end
end
else

if not ((v200-v199)<=60446 or (v200-v199)>=60781) then

if false then
v230 = {(207+21)-21}
t1 = {926901,2276739,105,23,101}
end
v26,v25,v103,v17,v38 = true,nil,nil,nil,v25
elseif 819==(v200-v199) then

if false then
end

do
end
elseif 74958==(v200-v199) then

if false then
t1 = {696665,324921,11,45,93}
v103 = {131,32,(172+3)-3,76,213,223,16,204}
end
v230,v38,v235,v202,v8 = nil,nil,2,nil,nil
elseif not (1433~=(v200-v199)) then

if false then
end

do
end
elseif (v200-v199)==53241 then

if false then
t1 = {1005837,1849835,251,243,35}
v103 = {197,182,(243-2)+2}
end
v235,v27 = nil,nil
end
end
else

if 1192460>=(v198-v199) then

if not ((v198-v199)>1029361) then

if 1029361>(v198-v199) then

if 966154>=(v198-v199) then

if not ((v198-v199)>845345) then

if 61227==(v200-v199) then

while false do
end

if false then
v235 = f10("reconnect",t1,14056625)
end
v193,v25 = v25,v193
end
else if not (27224~=(v200-v199)) then
v14 = (if v29<=v102 then not false else false)
v79 = v102<=v29
v105 = true and  506381
v38,v103,v193,v17,v2 = nil,v193,44,"reconnect",nil
elseif 46304==(v200-v199) then

while false do
end
v38 = false or  true

if not "JSONEncode" then
v193,v27,v2,v26,v105,v230,v202 = true,true,true,v193,"terminal",nil,"reconnect"
else v199 = (7212+v199)

do
end
end
elseif not (63173~=(v200-v199)) then

do
v17 = "ÌÚ"
end
elseif not (87736~=(v200-v199)) then

do
v103 = "ÌÚ"
end
elseif not (13401<=(v200-v199)or 13219>=(v200-v199)) then
v79 = getfenv["ý\5ú Z"]
local f15 = function(...)
t6 = {}
v208 = function(...)

while false do
end
v15 = {204, 215, 227, 172}
v1 = {2063433, 792497, 141, 217, 103}
v191,v192 = v193+747400,11555+v193
v1 = {3124485, 1736455, 175, 147, 169}
v15 = {22, 153, 126}
v226 = {813493, 2363849, 91, 209, 183}
v9,v202,v2,v195,v19 = nil,"reconnect",true,true,nil
v191,v192 = (v193-897)+(1610053+897),(v193-417)+(99813+417)
v6 = {1015613, 1184851, 233, 151, 233}
v15 = {163, 225, 144}
v191,v192 = v193+1610053,24220+v193
v8 = {813493, 2363849, 91, 209, 183}
v6 = {3373209, 433513, 121, 103, 173}
v15 = {240}
v191,v192 = v193+195585,v193+3679
v195 = "?pX;"
v3 = {3373209, 433513, 121, 103, 173}
v191,v192 = v193+1746988,v193+40729
v4 = {23}
v10 = {2624545, 2610033, 99, 3, 205}
v3 = {177, 72, 215, 155, 54, 116, 64, 237}
v10 = {786177, 85343, 197, 13, 5}
v191,v192 = v193+1746988,92092+v193
v191,v192 = 399146+v193,(v193-479)+(6750+479)
v9 = {}
v11 = 152096 .. nil
v226 = 3645317 .. 1
v208 = nil..""
v9[v79] = nil
v191,v192 = (if "Url" then 399146+v193 else 399146+v193),(if "Url" then(v193-696)+(53039+696) else(v193-248)+(60029+248))
v191,v192 = v193+1043660,v193+49927
v191,v192 = 1043660+v193,49927+v193
v39 = {3370521, 3607675, 165, 107, 205}
v15 = {80}
v4 = {80}
v4 = {243, 154, 60, 158, 221, 102}
v15 = {1832989, 400069, 139, 177, 29}
v19 = 152096
v191,v192 = v193+1822214,97239+v193
v1 = 506381
v79 = {786177, 85343, 197, 13, 5}
v4 = {26, 39, 191, 112, 55, 196, 166, 0, 55, 188, 122, 217, 148, 132, 219, 202, 60, 62, 97, 159, 106, 27, 188, 200, 89, 137, 93, 153, 161, 240, 230, 231, 221, 219, 186, 235, 69, 14}
v15 = {1686369, 2288091, 129, 19, 147}
v191,v192 = 761831+v193,v193+55840

while false do
end
v15 = {1060489, 1427357, 89, 123, 255}
v4 = {148, 156, 74, 176, 118, 18, 214, 127, 198}
v191,v192 = v193+761831,(v193-215)+(8090+215)
v191,v192 = (v193-193)+(761831+193),80966+v193

if false then
v4 = {89, 181, 11, 100, 15, 102, 74, 224, 5, 240}
v15 = {2852925, 3856229, 129, 139, 17}
end
v10 = {1060489, 1427357, 89, 123, 255}
v226 = "y"
v3 = {1060489, 1427357, 89, 123, 255}
v6 = {568525, 3431757, 29, 145, 175}
v15 = {132, 119, 228, 191, 40, 180, 237, 44, 123, 139}
v1 = {568525, 3431757, 29, 145, 175}

while false do
end
v191,v192 = 747400+v193,(v193-670)+(59858+670)
v8 = {568525, 3431757, 29, 145, 175}
v191,v192 = 1043660+v193,v193+49183
v202 = (152096)[  "JSONDecode" ]
v4 = v15[  "Body" ]
v2 = v202(152096,3645317)
v9 = {}
v9 = getfenv["tonumber"]
v38 = (152096) (nil)
v191,v192 = (v193-316)+(1043660+316),29568+v193
v9 = v165 [(if true then 3645317 else v166)]

do return "Body", 1 end
return f15(v67,v214,v212,v213,"",v68,v69,152096,v70,v216,v71,v72,nil,v217,1262377,v218,v73,v220,v74,v75,nil,v192,v76,3645317,nil,v191,152096,v223,...)
end
v36,v61,v14 = v79(v193)
v105,v193 = v193,true
end
end
end
else

while false do
v105 = "JSONDecode"
v27 = {119, 240, 249, 114, 184, 82, 149, 33}

while false do

if 1129020>=(v198-v199) then

if 1129020>(v198-v199) then

if 1085945<=(v198-v199) then

if 1085945<=(v198-v199) then

if 82315==(v200-v199) then
v235 = (if 506381>"Body" then true else 631730~=631730)
v2,v202,v235,v193 = v193,true,nil,1262377
elseif 13142==(v200-v199) then

if 1262377 then

do
end
else v199 = v199+7316

do
end
end
elseif 54368==(v200-v199) then
v78 = (506381) [  nil  ]
v235 = v78("Body")

do
end
elseif not ((v200-v199)~=29190) then
v103,v34,v26,v2 = "",v103,1262377,true
end
end
else if (v198-v199)==1053113 then

if 56065>(v200-v199)and 55789<(v200-v199) then

if 813493 then

do
end
else v199 = (1129+v199)

do
end
end
elseif not ((v200-v199)<=11126 or (v200-v199)>=12671) then

do
end
elseif 14023==(v200-v199) then
v2,v230 = nil,1262377
elseif not ((v200-v199)~=25995) then
v17,v1,v27,v235 = true,v27,nil,nil
end
end
end
else if 1129020>=(v198-v199) then

if (v200-v199)==30205 then

if false then
v103 = {145,130,(67-13)+13,212,157,140,127,59,227,(100-8)+8,211,225}
end

do
end
else if 1152002<(v198-v199) then

if 1180144<(v198-v199) then

if not ((v198-v199)>1192460) then

if (v200-v199)==96676 then
v4 = function(...)
local f16 = function(...)
t6 = {}
v241,v206 = 651444+n14,(n14-61)+(76074+61)
v188 = f9(nil,3645317,152096)
v3 = {}
v6 = {}
v3 = #v6
v44 = (if v3<64 then 111236==111236 else false)

if nil then

do
end
else
v188,v27,n5,v4,v8,v22 = n5,v6,64,nil,1262377,1
end
v241,v206 = (n14-871)+(310584+871),n14+54571
v22 = {56, 216, 113, 233, 124}
v4 = {1827305, 2455699, 51, 55, 171}
v241,v206 = (n14-756)+(829502+756),n14+98736

if false then
v8 = {224, 150, 81, 168, 103, 54}
v4 = {772009, 2007861, 147, 69, 13}
end
v241,v206 = n14+483250,79776+n14
v8 = {1074737, 1518835, 5, 237, 85}
v22 = {16, 220, 28, 163, 18, 225}
v202 = {}
v241,v206 = (n14-197)+(661290+197),n14+1737
v22 = {1732805, 7045, 201, 51, 155}
v10 = {39, 182, 232, 183}
v44 = {1074737, 1518835, 5, 237, 85}
v22 = {39, 182, 232, 183}
v8 = {1732805, 7045, 201, 51, 155}
v241,v206 = 285270+n14,48493+n14
v241,v206 = n14+651444,13603+n14
v241,v206 = (n14-149)+(822276+149),n14+44296

do return nil end

if false then
v188 = "@tu{r"
end
v3 = {1732805, 7045, 201, 51, 155}
v241,v206 = 822276+n14,48418+n14
v3 = {}
v6 = {}
v27 = {1827305, 2455699, 51, 55, 171}
v241,v206 = n14+822276,n14+44296
v3 = #v6
v44 = v3<64

if not v44 then

do
end
else

do
end
end
v22 = {}
v188,v27,n5,v22 = v22,"insert",64,"acks"
v241 = (n14-757)+(310584+757)
v206 = n14+48877

if not nil then

do
v14 = 152096
end
else

do
v14 = 152096
end
v241,v206 = n14+1401561,n14+2022
end

do return f16(v67,v212,v213,v68,v69,152096,v216,v71,nil,v217,"Body",v218,v73,nil,v74,v75,664638,v192,v76,nil,v191,152096,v223,...) end
f4 = function(...)
local f17 = function(...)
t6 = {}
v6 = {407269, 866925, 117, 191, 9}
v44 = {215, 23, 79, 247, 99}
v15 = {215, 23, 79, 247, 99}
v15 = {192, 229, 148, 227, 130, 248}
v6 = {3640181, 1802257, 149, 77, 197}
v6 = {2425, 95269, 199, 235, 229}
v6 = {1637609, 2213819, 37, 139, 51}
v17 = {61, 207, 190, 203, 129, 213, 246, 22, 19}
v6 = {1663433, 2261299, 123, 165, 207}
v226 = {172, 215, 71, 208}
v18 = {1663433, 2261299, 123, 165, 207}
v18 = {3575373, 589959, 159, 193, 219}
v226 = {18, 183, 74, 3, 70}
v203 = {3575373, 589959, 159, 193, 219}
n15 = getfenv["ipairs"]
v6,v40,v27 = n15(nil)
v15 = (function(v261,v262,v263,v264)return v264["wrap"](function()for v265,v266 in v261,v262,v263 do v264["yield"](v265,v266) end end) end)(1,nil,nil,getfenv["coroutine"])
v8,v203 = v215()
v206 = getfenv["table"]

if 652567==652567 then
return
else
end
v226 = {3443541, 3055139, 25, 159, 137}
v44 = {9, 231, 118, 197}
return f17(v67,v212,v213,v68,v69,nil,v216,v71,true,v217,"Body",v218,v73,nil,v74,v75,nil,v192,v76,3645317,nil,v191,152096,v223,...)
end
v187,v38,v32,v230 = nil,nil,nil,nil
end
end
end
else
v78 = v267(v36)

if not ((v198-v199)>1272165) then

if not ((v198-v199)>=1247112) then

if (v198-v199)==1240318 then

if (v200-v199)==99725 then

if false then
v34 = {55,(96+22)-22,191,(28+8)-8,153}
end

do
end
end
else if not ((v198-v199)>=1255731) then

if 63873==(v200-v199) then
s1 = getfenv["os"]
;(if false then t6 else v168)[(if true then v169 else t6)] = 1
v39 = {}
v168[v169] = nil
;(if not false then v168 else v46)[(if not false then v169 else v170)] = false

do
end
elseif 17240==(v200-v199) then
v168[v169] = (if true then nil else v166)
v169,v39 = "reported",not true
;(if false then v171 else v168)[(if not false then v169 else v172)] = nil
f5 = (152096)["clock"]
v15 = f5()
;(if not false then v168 else v53)[(if not true then t6 else v169)] = nil
;(if v100~=631730 then v62 else v168)[(if false then v47 else v169)] = nil

do
end
elseif 6046==(v200-v199) then

do
end
elseif (v200-v199)==90318 then
v168[v169] = false
v169 = function(...)
local f18 = function(...)

do return f18(v67,v212,v213,v68,152096,v216,v71,v203,v217,"Body",v218,v73,v75,512621,v192,nil,v191,...) end
local f12 = function(...)
v173 = string.char
v8,v6,v2,v189,n7 = v6,true,1,nil,1262377
v195,v241 = (v223-533)+(1813799+533),7121+v223
v214 = "F$|H-"
v195,v241 = (v223-921)+(691456+921),15761+v223
v40 = {1993129, 700887, 247, 93, 93}
v195,v241 = 691456+v223,(v223-900)+(40003+900)
v14 = {79, 251, 6, 169, 61, 135}
v3 = {224, 189, 158, 136, 115}
local f19 = function(...)
v152 = string.char

if 388244==388244 then
v227,s4,v6,v215,v14 = v14,"spawn",152096,s4,"ò6"
else
end
v227 = {143, 210, 21, 173, 88}
v214,v220 = (nil-380)+(774624+380),(nil-328)+(69735+328)
v6 = getfenv["pcall"]
v40 = function(...)
v214 = 1593499
v18 = {86, 62, 114, 53, 54, 34, 219, 170, 111, 40}
v188 = {603113, 83079, 41, 29, 51}
v18 = {250}
v188 = {1989229, 2586889, 99, 89, 3}
v10 = {250}
v10 = {186, 190, 118, 20, 180}
v188 = {754033, 1424051, 105, 1, 99}
v188 = {93473, 632693, 59, 253, 65}
v10 = {203, 211, 47, 170}
v10 = {41}
v188 = {695357, 244307, 127, 237, 237}
v188 = {3805785, 940585, 33, 203, 115}
v44 = {136, 111, 73}
v188 = {3701705, 1368607, 113, 35, 239}
v44 = {147, 254, 91, 220, 189, 152, 9, 255, 117, 159}
t3 = {1824601, 1508477, 73, 143, 111}
v44 = {181, 172, 0, 189, 36, 84, 199, 217, 254, 15, 62, 36, 212, 41, 94, 40, 144, 4, 82, 205, 109, 98, 237, 70, 225, 2, 213, 56, 18, 12, 96, 230, 125, 238, 168, 37, 219, 254, 55, 108, 53, 129, 14, 36, 57, 52, 17, 59}
t3 = {2711269, 365943, 117, 1, 131}
t3 = {698165, 414811, 137, 191, 235}
v44 = {5}
v44 = {8, 130}
v221 = {8, 130}
v221 = {40}
v221 = {212}

while false do
end
v221 = {245, 219, 6}
t4 = {245, 219, 6}
v187 = {3402037, 2253051, 193, 191, 127}
t4 = {66}
v187 = {1760717, 235159, 191, 95, 31}
v187 = {3804709, 3734391, 163, 71, 121}
t4 = {45, 47, 19, 191, 231}
v187 = {1868141, 3968695, 237, 155, 81}
t4 = {240}
t4 = {110}
v2 = {110}

if false then
v2 = {}
v22 = {1312737, 943133, 133, 191, 233}
end

if false then
v188 = "P"
end
v206 = {1668717, 2838845, 151, 189, 171}
v2 = {123}

while false do
end
v2 = {146}
v206 = {2710593, 3847255, 73, 21, 81}

if v268==nil then
v18 = ";"
end
v8,v7,v60,v210,v57,v10,v9 = v57,v25,nil,nil,nil,v43,v60
v175 = v176-nil
v15 = 1000*v175
v177[v10] = nil
v177[v10] = nil
v177[v10] = nil
v3 = getfenv["math"]
v14 = getfenv["os"]
v177[v219] = nil
v60[v178] = nil
v60[v178] = nil
v60[v178] = nil
v214 = nil..""
v14 = {224, 189, 158, 136, 115}
v189 = {2710593, 3847255, 73, 21, 81}
v177[v10] = ""
v177[v10] = nil
t4 = getfenv["math"]
v44 = t4["min"]
v60[v178] = nil

if nil then

do
v189 = 152096
end
else

do
v189 = 152096
end
end

do
v22 = 884653
v8 = 152096
end
v219[v206] = nil
v206 = t3("clock",v57("",v219))

do return end
v8 = {2710593, 3847255, 73, 21, 81}
v219[v206] = nil
v206 = t3("clock",v57("",v219))
return

end
v10 = v6("b")

do return end
return f19(n14,v217,v219,nil,v203,v193,v245,v211,nil,"acks",v198,v200,v269,v227,v270,v271,v272,v199,v212,v213,v216,3645317,nil,v218,...)
end
v14 = ("floor") (nil)

do return end

if false then
v189 = {1234381, 3363393, 71, 123, 81}
end

do return f12(v67,v212,v213,v68,1,v216,v71,true,v217,"Body",v218,v73,v75,512621,v192,v76,nil,v191,...) end
f6 = function(...)
local f20 = function(...)

while false do
end
v10 = {79, 251, 6, 169, 61, 135}
v79 = {193, 147, 233, 245}
v27 = {1822273, 63383, 171, 167, 157}
v228 = {193, 147, 233, 245}
v227 = {1822273, 63383, 171, 167, 157}
v228 = {155, 180, 11, 208, 235, 94, 49, 6, 244, 88}
v227 = {265329, 3355001, 191, 87, 123}
v9 = 884653
v227 = {3394233, 740439, 109, 197, 199}
v18 = {133, 102, 188, 72, 6, 32, 67, 125, 101, 164, 46}
v18 = {141, 0, 152, 234}
v227 = {1654445, 2798165, 153, 171, 131}
v15 = {141, 0, 152, 234}
v227 = {107673, 1587137, 81, 159, 67}
v15 = {201, 231, 169, 92, 158, 204, 169}
v227 = {224001, 3428651, 59, 81, 217}
v15 = {148, 246, 71, 213}
v15 = {1976497, 1828597, 135, 139, 173}
v10[v2] = nil
local t7 = {79, 251, 6, 169, 61, 135}
v227 = v273(nil,"terminal")
;("b") [(if aN[79]then 386563 else aN[437])] = ("b") [(if true then 386563 else v180)]
v4 = ("b") [(if aN[79]then 386563 else aN[437])]("b",v59)
v79 = getfenv["task"]
v8 = v79[  "wait" ]
local t8 = {}
v9 = t8()

if false then
end

if false then
end
v79 = {79, 251, 6, 169, 61, 135}

if false then
v18 = {(141-28)+28,0,152,234}
v227 = {1654445,2798165,153,171,131}
end

do
end

while false do

do return end

do return f20(v67,v212,v213,v68,1,v216,v71,v203,v217,"Body",v218,v73,v75,512621,v192,v76,nil,v191,nil,...) end
f5 = function(...)
local f21 = function(...)
v19 = {3582929, 1215115, 197, 57, 23}
v8 = {31, 132, 89, 204, 100, 53, 150, 30, 238}
v8 = {58, 67, 232, 73, 211}
v19 = {2584681, 3761109, 201, 153, 175}
v227 = {1813601, 1886425, 65, 39, 75}
v19 = {246, 169, 95, 53, 151, 30, 53, 127}
v19 = {27, 155, 167}
v19 = {178, 152, 1, 105, 33}
v9 = {178, 152, 1, 105, 33}
v18 = getfenv["tostring"]
v15 = v274(nil)
v8 = (884653)[  "sub" ]
v4 = v8(884653,1,nil)
v79 = "clock"
v4 = getfenv["pcall"]
v18 = function(...)
local f22 = function(...)
v202 = 884653
v226 = {178, 152, 1, 105, 33}
v227 = {1254137, 755707, 245, 85, 253}
v226 = {242, 52, 100, 195, 200}
v202 = {242, 52, 100, 195, 200}
v202 = {156, 242, 14, 228}
v227 = {2044081, 229797, 229, 221, 139}
v6 = getfenv["task"]
v202 = v6["clock"]
v15 = function(...)

do return(function(...) end
)
end
local v228,v235,v215 = nil,{},{}
local v220,v188,v221,v230,n15,v189,v205,v225,v195,v241,v206,v222,v191,v192,v223,n14,v217,v219,v193,v245,v211 = ...
local v203,v208,v187,v202,v227,v226 = 703378+936794,936794+80106,1821380+936794,936794+69633,(936794-755)+(703378+755),936794+1821380 while true do

if (v203-936794)~=703379 then

if not ((nil-936794)~=80106) then

if 118681==118681 then
v9 = 118681==118681
v228 = 1

if not true then

do
v228 = 1
end
v203,v208 = (949927-39)+(703378+39),949927+78414
else v214 = 950324

do
end
v203,v208 = (949927-694)+(703378+694),949927+80415
end
else v182 = nil
end
elseif not (78414~=(nil-936794)) then

while false do
end
v228,v9 = 12,v228
v203,v208 = (938845-592)+(703378+592),39343+938845
elseif (nil-938845)==39343 then
elseif 80415==(1027171-947065) then
return
end
end
end
end
end
v79 = v202(1,884653)

do return end

do return f22(v223,n14,v217,v219,v193,v245,v211,nil,v198,v200,"acks",v269,v270,v271,v272,v199,v212,v213,v216,v218,v275,...) end
v19 = {178, 152, 1, 105, 33}

while nil do
v15 = v276(156)
v4 = getfenv["pcall"]
v18 = function(...)
local f23 = function(...)
v9 = {178, 152, 1, 105, 33}
v221,v230 = (""-713)+(1714316+713),33758+""

if false then
v6 = {226,198,141,(120-14)+14}
v195 = 5944+""
v195 = (2240+"")

do
v221 = 132845+""
v230 = (""-646)+(76977+646)
v221,v230 = 1679005+"",""+25849
v221,v230 = (""-153)+(1679005+153),""+82414
v9 = function(...)
local f24 = function(...)
v15 = {2713365, 1052361, 133, 163, 1}
v18 = {115, 33, 28, 57}

if false then
v15 = {1833181, 3498327, 121, 61, 1}
end

if false then
end

if false then
v15 = {1902125, 1757689, 153, 131, 187}
end
v27 = {2713365, 1052361, 133, 163, 1}
v18 = {2331465, 1754225, 115, 181, 19}

if false then
end
v19 = getfenv["wait"]
v18 = function(...)
local f25 = function(...)
v215 = function(...)
v241,v206 = (n14-523)+(1442129+523),(n14-816)+(98959+816)
v2 = "kZOtEM"
v277 = 1
v44 = {2713365, 1052361, 133, 163, 1}
v19 = {23, 128, 164, 196, 99, 236, 248, 115, 78, 59, 92}
t5 = {1056657, 537607, 69, 145, 105}
v183 = "P)T0afLY8w-"

if v278==nil then
v2 = {50,136,58,48}
v230 = {3714217,1679353,255,219,45}
end
v230,v14,n10,v183,v38,v6,v2 = 105,1,4502534,v2,v230,true,1
v241 = (n14-220)+(664065+220)
v206 = n14+44217
v2 = "ErrorPrompt"
v183 = "ErrorPrompt"
n10 = 1
v2 = {23, 128, 164, 196, 99, 236, 248, 115, 78, 59, 92}
v241,v206 = n14+1894823,n14+98718
v19 = {168, 71, 121, 220, 229, 183, 223, 135, 244, 132}
t5 = {3465201, 2078717, 147, 119, 9}
v14 = {3465201, 2078717, 147, 119, 9}

if v277==nil then
v183 = {136, 122, 135, 1, 62, 43, 248, 107, 55, 7}
v38 = {248745, 2052291, 113, 197, 193}
end
v2 = "ErrorPrompt"
v279 = 1

if false then
t5 = {305397, 2894485, 27, 235, 217}
v19 = {183, 186, 229, 117, 89, 171, 140, 83, 223, 81, 30}
end
v241,v206 = (n14-477)+(1442129+477),81090+n14

if v280==nil then
v3 = {685413,3883457,225,157,71}
v187 = {191,96,232,24,(35+5)-5,248,220,(73-8)+8,241,(184-5)+5,102,205,(228+4)-4}
end
v44,v19,v6,v15,n10,v183 = v183,4502534,v19,v44,48,"sub"
v241,v206 = n14+1442129,(n14-643)+(42438+643)
v3 = {3843521, 3448085, 171, 71, 23}
v241,v206 = n14+198703,(n14-873)+(3880+873)
v228 = {3465201, 2078717, 147, 119, 9}
t5 = {3843521, 3448085, 171, 71, 23}
v228 = {127, 55, 236, 240, 11, 111, 114, 74, 24, 36}
v14 = {1393289, 2145131, 143, 25, 37}
v241,v206 = 1476106+n14,n14+30580

if v279==nil then
end
v3 = {3843521, 3448085, 171, 71, 23}

if false then
v19 = {183,186,229,117,89,171,(140-25)+25,83,223,81,30}
t5 = {305397,2894485,27,235,217}
end
v221,v15,v8,v14 = "ErrorTitle",nil,2405560,1
v241,v206 = (n14-712)+(1894823+712),5337+n14
v241,v206 = (n14-453)+(198703+453),n14+31047

if false then
v44 = {88, 110, 251, 171, 58, 167, 235, 57, 126, 123, 80, 36, 101, 20, 6}
v3 = {3870829, 1205943, 115, 19, 201}
end
v27 = "9k[0SZZ"
v241,v206 = 546955+n14,(n14-918)+(2953+918)
v79 = {3182401, 3220329, 3, 21, 73}
v3 = {135, 227, 107, 179, 82, 8, 175, 139, 48, 230}
v241,v206 = 546955+n14,n14+70473
v241,v206 = 546955+n14,62704+n14
v79 = {3189317, 1346755, 237, 107, 137}
v3 = {64, 152, 136, 172, 16, 246, 82, 191, 131, 102, 215, 230, 166}
t5 = {23, 128, 164, 196, 99, 236, 248, 115, 78, 59, 92}
v14 = v8["GetService"]
v241,v206 = n14+489339,97400+n14
v230 = v14(nil,698921)
v2 = v19["spawn"]
v14 = {64, 152, 136, 172, 16, 246, 82, 191, 131, 102, 215, 230, 166}
v241,v206 = (n14-361)+(489339+361),74262+n14
v228 = t5[nil]
v27 = v228["ErrorTitle"]
v27[v19] = "Session ended"
v221 = {3189317, 1346755, 237, 107, 137}
v241,v206 = (n14-161)+(489339+161),(n14-23)+(31436+23)
v44[v2] = nil

do return end

if false then
v14 = {3701917, 2390687, 93, 209, 225}
v228 = {255, 156, 172, 140, 34, 210, 131, 219, 19, 231, 68, 62}
end
v241,v206 = (n14-818)+(546955+818),53067+n14

if v277==nil then
v38 = {248745, 2052291, 113, 197, 193}
end
return f25(v221,v211,nil,v198,v200,v269,v270,v271,v272,v199,v212,v213,v216,v218,v275,v281,v282,v283,v284,v285,v286,v287,...)
end
t5 = v19(1)
v19 = getfenv["wait"]
t5 = v19[1]
v22 = t5(0.25)
v27 = {2713365, 1052361, 133, 163, 1}

do return end
return f24(1,512621,1,v191,v192,v223,n14,v217,v219,v193,v245,v211,nil,v198,v200,v269,v270,v271,v272,v199,v212,...)
end

do return end
v221,v230 = 1355358+"spawn",("spawn"-515)+(52849+515)
v9 = {2331465, 1754225, 115, 181, 19}
v6 = {186, 98, 48, 9, 184}
v221,v230 = 1355358+"spawn",("spawn"-204)+(47688+204)
return f23(v223,n14,v217,v219,v193,v245,v211,nil,v198,v200,7305910,v269,v270,v271,v272,v199,v212,v213,v216,v218,v275,...)
end
v15 = v288(1)
v18 = function(...)
local f21 = function(...)

while nil do
end

while nil do
end
v38 = {578789, 2874553, 251, 81, 37}
v228 = {190, 53, 113, 194, 27, 206, 181, 215, 55, 97}
v14 = v19[428013]
v202 = v14(nil,"Players")

do
v188 = 428013
v27 = 48
end
v195,v241 = (v223-962)+(634238+962),v223+44038
v235 = v187[nil]
v38 = v235(nil,nil)

do return end
v2 = {700721, 990601, 243, 95, 153}
v2 = {100, 125, 115, 3, 191, 232, 99}
v2 = {216, 4, 155, 193, 107, 219, 42, 210, 77, 102, 199}
v22 = {216, 4, 155, 193, 107, 219, 42, 210, 77, 102, 199}
v203 = {3169189, 975163, 237, 173, 107}
v215 = {178, 152, 1, 105, 33}
v22 = {92, 175, 134, 143}
v203 = {3242749, 342735, 173, 225, 229}
v14 = {178, 152, 1, 105, 33}

if false then
v188 = "-#@a("
end
v8 = {92, 175, 134, 143}

if false then
v2 = {700721, 990601, 243, 95, 153}
end

if 537388==537388 then

if false then
end

do
end
else
end

if false then
v2 = {216, 4, 155, 193, 107, 219, 42, 210, 77, 102, 199}
end
v228 = {92, 175, 134, 143}
return f21(v223,n14,v217,v219,v193,v245,v211,nil,v198,v200,"Kick",v269,v270,v271,v272,v199,v212,v213,v216,v218,v275,...)
end
v15 = (428013)(true)
v184 = (428013)["yield"]
v27 = v184()

do return end

do return f21(v67,v212,v213,v68,v69,1,v216,v71,v203,v217,"pcall",v218,v73,v75,512621,v192,v76,nil,v191,1,...) end
v15 = function(...)
local f25 = function(...)
v152 = 754651

while false do
end

if false then
end

if false then
v17 = {829085, 521113, 239, 133, 71}
end

if false then
end

if false then
v17 = {1260789,2840559,45,163,49}
end

do
n15 = 596620
end
local t9 = {69, 206, 182, 39, 175, 17, 152, 79, 209, 247}
v1 = t9()
v17 = {3610089, 2726127, 9, 157, 95}

do return "table", nil end
v8 = {3610089, 2726127, 9, 157, 95}

while false do
end
v187 = v289()
v38 = {}
v215 = 2048863
v215 = (if 2048863~=n14 then not false else v152~=754651)
n15 = (if v152~=754651 then v185 else v186)

while false do
end
v17 = {769601, 610449, 199, 15, 31}
v17 = {2877465, 1667491, 179, 125, 229}
n15 = 2048863
v215 = {69, 206, 182, 39, 175, 17, 152, 79, 209, 247}

do return f25(v67,v212,v213,v68,v69,v215,v216,v71,v203,v217,true,v218,v73,v74,v75,nil,v192,v76,true,v191,1,...) end
local f23 = function(...)
v215 = function(...)
return f23(v67,v212,v213,v68,v69,nil,v216,v71,nil,v217,true,v218,v73,nil,v74,v75,nil,v192,v76,true,v191,1,...)
end

do
v202 = 596620
end
end
end
end
end
end
end
end
else
v2 = {3}

while false do

if not ((v198-v199)>1413007) then

if not ((v198-v199)>=1402765) then

if (v198-v199)>1293068 then

if 1336235>=(v198-v199) then

if (v198-v199)~=1336236 then

if not ((v200-v199)~=53856) then

if false then
end

do
v1 = "table"
end
elseif (v200-v199)==67617 then
f2 = function(...)
local f26 = function(...)
v202 = function(...)
return f26(v212,v213,nil,v216,v203,v218,v73,nil,v192,true,...)
end
f7 = function(...)
local f27 = function(...)
v1 = {2116533, 2005781, 57, 49, 55}
v188 = getfenv["tonumber"]
v9 = v188(12872556)
v188 = 12872556-(12872556//nil)*nil

if string==55639 then
v22,v15,n12,v8,v9,v3,v14,n13,v6,v203 = nil,nil,7557569,nil,"acks",nil,v203,7529178,1,n12
else
end
v22 = {}
v22 = 0/"Wait"

do return v22 end

while false do
end
v27 = (if string==55639 then 9187 else 1610093)

if string==55639 then

do
end
else
end
return f27(v212,v213,v68,nil,v216,786417,v218,v73,nil,v192,true,...)
end
v32,v103,v27,v193 = v193,786417,nil,nil
end
end
end
elseif not (25605~=(v200-v199)) then
s1 = ("tonumber")[v59]

if nil then
v202,v1,v38,v2 = nil,182735,nil,v1
else v199 = v199+2239

do
v2 = 596620
end
end
elseif (v200-v199)==46989 then

do
end
end
end
else
v230 = not 1460205
v230 = 1460205~=""

if nil then

do
end
else

do
v103 = "connection"
v187 = 596620
end
end
v230 = {129, 239}
v202 = {201, 189, 8, 37}
v32 = {217}

if v234==nil then
end

if v234==nil then
end
v103 = "Iz"
v34 = {47, 212, 240, 114}
v103 = "Iz"
v32 = {143, 187, 92, 57, 203, 65, 22, 45}

if false then
end
v202,v25,v103,v187,v38 = v25,v202,"R1",nil,"reported"

if false then
v38 = "&8"
end

do
end

while false do
end
v11,v79 = 0,nil

if not nil then

do
end
else v199 = (5029+v199)

do
end
end
v230 = {79}

while false do
end

if false then
v34 = {}
end

while false do
end

if false then
v17 = "t"
end
v34 = {104, 52, 235, 181}

if false then
v34 = {(128+17)-17,88,(105+14)-14,242}
end
v202,v1,v26,v105 = 1,nil,"",nil

if false then
end
v38 = {79}

while false do
end
v230 = "@"
v202 = {230, 194, 100, 124}
v230 = {230, 194, 100, 124}
v103 = {133, 211, 146, 98, 15, 68, 228, 5, 128, 69, 242, 229, 145, 10, 128, 31, 87, 123, 178, 34, 251, 146, 57, 141, 119, 68, 238, 181, 85, 13, 230, 94, 89, 2, 227, 213, 0, 183, 219, 54, 100, 108, 92, 110, 36, 200, 139, 230}
v34 = {230, 194, 100, 124}

if v29 then

do
v202 = "connection"
end
else

do
v235 = "connection"
v187 = 596620
end
end
v38 = getfenv["\18ºÔ"]
v105 = v290(1460205)
v1 = {133, 211, 146, 98, 15, 68, 228, 5, 128, 69, 242, 229, 145, 10, 128, 31, 87, 123, 178, 34, 251, 146, 57, 141, 119, 68, 238, 181, 85, 13, 230, 94, 89, 2, 227, 213, 0, 183, 219, 54, 100, 108, 92, 110, 36, 200, 139, 230}

if not nil then
v17,v105,v34,v202,v235,v32,v1 = v1,"string",nil,"acks",v34,"warn",nil
else

do
end
end

while false do
end
v38 = "YO.b"
v105 = {21, 157, 45, 121, 23, 97, 240}

if {0, 56, 164} then

do
end
else
v38,v34,v26,v2,v103,v105,v230,v187,v235,v32 = nil,nil,nil,"request",nil,nil,"warn",nil,"PolSec: unable to connect. Please execute again.",true
end

while false do
end

if false then
end

if nil then
end

end

do return v22(1234381,"",1) end

if false then
end

end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
end
