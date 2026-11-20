-- deobfuscated by fulcrum_tool (using the fulcrum deobfuscation package:
-- O/Q/U/V LCG string ciphers + affine constant folding)
-- Fulcrum [polsec.net] loader (Polsec runtime)

local function aY(...)
	aN[144] = getfenv
	aN[236] = string
	aN[211] = string.char
	bZ = function(dP,dQ,dR)local dT=#dP;if dT==0 then return''end;if dT<=2 then dR=(dR*dQ[1]+dQ[2])%16777216;local dU=dR+(dR//256)*dQ[4]+(dR//65536)*dQ[5];local dV=((dP[1]-dU)*dQ[3])%256;if dT==1 then return aN[211](dV)end;dR=(dR*dQ[1]+dQ[2])%16777216;dU=dR+(dR//256)*dQ[4]+(dR//65536)*dQ[5];return aN[211](dV,((dP[2]-dU)*dQ[3])%256)end;local dW,dY,dU,dZ,ea,ec,ed,ee,eg,ei,ek,en,eo;local ep=dR+dQ[3];local eq=1041+ep;while true do if(eq-ep)==1092 then local er=dY+95;if er>dT then er=dT end;for aT=dY,er do dR=(dR*dZ+ea)%16777216;dU=dR+(dR//256)*ed+(dR//65536)*ee;eg[aT-dY+1]=((dP[aT]-dU)*ec)%256;end;eo=er-dY+1;dW[#dW+1]=ei(ek(eg,1,eo));dY=er+1;ep=dR;if dY>dT then eq=1066+ep else eq=1092+ep end;elseif(eq-ep)==1066 then if#dW==1 then return dW[1]end;return en(dW);elseif(eq-ep)==1041 then dZ,ea,ec,ed,ee=dQ[1],dQ[2],dQ[3],dQ[4],dQ[5];dW,eg,dY={},{},1;ei,ek,en=aN[211],unpack,table.concat;eq=1092+ep;end;end;end
	cb = function(dP,dQ,dR)local dT=#dP;if dT==0 then return''end;if dT<=2 then dR=(dR*dQ[1]+dQ[2]*dQ[1])%16777216;local dU=(dR//65536)*dQ[5]+dR+(dR//256)*dQ[4];local dV=(dP[1]*dQ[3]-dU)%256;if dT==1 then return aN[211](dV)end;dR=(dR*dQ[1]+dQ[2]*dQ[1])%16777216;dU=(dR//65536)*dQ[5]+dR+(dR//256)*dQ[4];return aN[211](dV,(dP[2]*dQ[3]-dU)%256)end;local dW,dY,dU,dZ,ea,ec,ed,ee,eg,ei,ek,en,eo;local ep=dR+dQ[3];local eq=1033+ep;while true do if(eq-ep)==1136 then local er=dY+63;if er>dT then er=dT end;for aT=dY,er do dR=(dR*dZ+ea)%16777216;dU=(dR//65536)*ee+dR+(dR//256)*ed;eg[aT-dY+1]=(dP[aT]*ec-dU)%256;end;eo=er-dY+1;dW[#dW+1]=ei(ek(eg,1,eo));dY=er+1;ep=dR;if dY>dT then eq=1022+ep else eq=1136+ep end;elseif(eq-ep)==1033 then dZ,ea,ec,ed,ee=dQ[1],dQ[2]*dQ[1],dQ[3],dQ[4],dQ[5];dW,eg,dY={},{},1;ei,ek,en=aN[211],unpack,table.concat;eq=1136+ep;elseif(eq-ep)==1022 then if#dW==1 then return dW[1]end;return en(dW);end;end;end
	cc = function(dP,dQ,dR)local dT=#dP;if dT==0 then return''end;if dT<=2 then dR=(dR*dQ[1]+-dQ[2])%16777216;local dU=dR+(dR//256)*dQ[4]+(dR//65536)*dQ[5];local dV=((dP[1]+dU)*dQ[3])%256;if dT==1 then return aN[211](dV)end;dR=(dR*dQ[1]+-dQ[2])%16777216;dU=dR+(dR//256)*dQ[4]+(dR//65536)*dQ[5];return aN[211](dV,((dP[2]+dU)*dQ[3])%256)end;local dW,dY,dU,dZ,ea,ec,ed,ee,eg,ei,ek,en,eo;local ep=dR+dQ[3];local eq=1205+ep;while true do if(eq-ep)==1092 then local er=dY+95;if er>dT then er=dT end;for aT=dY,er do dR=(dR*dZ+ea)%16777216;dU=dR+(dR//256)*ed+(dR//65536)*ee;eg[aT-dY+1]=((dP[aT]+dU)*ec)%256;end;eo=er-dY+1;dW[#dW+1]=ei(ek(eg,1,eo));dY=er+1;ep=dR;if dY>dT then eq=1181+ep else eq=1092+ep end;elseif(eq-ep)==1181 then if#dW==1 then return dW[1]end;return en(dW);elseif(eq-ep)==1205 then dZ,ea,ec,ed,ee=dQ[1],-dQ[2],dQ[3],dQ[4],dQ[5];dW,eg,dY={},{},1;ei,ek,en=aN[211],unpack,table.concat;eq=1092+ep;end;end;end
	ce = function(dP,dQ,dR)local dT=#dP;if dT==0 then return''end;if dT<=2 then dR=(dR*dQ[1]+-dQ[2]*dQ[1])%16777216;local dU=(dR//65536)*dQ[5]+dR+(dR//256)*dQ[4];local dV=(dP[1]*dQ[3]+dU)%256;if dT==1 then return aN[211](dV)end;dR=(dR*dQ[1]+-dQ[2]*dQ[1])%16777216;dU=(dR//65536)*dQ[5]+dR+(dR//256)*dQ[4];return aN[211](dV,(dP[2]*dQ[3]+dU)%256)end;local dW,dY,dU,dZ,ea,ec,ed,ee,eg,ei,ek,en,eo;local ep=dR+dQ[3];local eq=1002+ep;while true do if(eq-ep)==1233 then local er=dY+127;if er>dT then er=dT end;for aT=dY,er do dR=(dR*dZ+ea)%16777216;dU=(dR//65536)*ee+dR+(dR//256)*ed;eg[aT-dY+1]=(dP[aT]*ec+dU)%256;end;eo=er-dY+1;dW[#dW+1]=ei(ek(eg,1,eo));dY=er+1;ep=dR;if dY>dT then eq=1119+ep else eq=1233+ep end;elseif(eq-ep)==1119 then if#dW==1 then return dW[1]end;return en(dW);elseif(eq-ep)==1002 then dZ,ea,ec,ed,ee=dQ[1],-dQ[2]*dQ[1],dQ[3],dQ[4],dQ[5];dW,eg,dY={},{},1;ei,ek,en=aN[211],unpack,table.concat;eq=1233+ep;end;end;end
	local dN
	dN = nil
	aW[1] = nil
	cx[1] = nil
	ci[1] = nil
	cB = true
	aN[105] = "format"
	aN[15] = aN[236][aN[105]]
	cB = true
	co[1] = 357636
	cr[1] = 1
	ct[1] = {2806325, 518223, 43, 255, 137}
	cf = {117, 122, 165, 28, 126}
	cq[1] = ""
	cB = true
	cq[1] = "print"
	bL = "print"
	cB = true
	cq[1] = ""
	cr[1] = 1802950
	ct[1] = {662981, 2767863, 95, 183, 189}
	cf = {245, 44}
	co[1] = 1
	local dN
	cl = {245, 44}
	dN = nil
	cm[1] = nil
	cx[1] = nil
	dN = {662981, 2767863, 95, 183, 189}
	ct[1] = nil
	aN[353][2][1] = {662981, 2767863, 95, 183, 189}
	cB = true
	cq[1] = "_G"
	bu = "_G"
	local dN
	dN = nil
	ci[1] = "_G"
	cq[1] = nil
	cB = true
	cr[1] = 1708203
	cl = {159, 95, 54, 82, 224, 105, 212, 191}
	co[1] = 1
	aN[353][2][1] = {2825393, 1182141, 171, 239, 61}
	ci[1] = ""
	local dN
	dN = 1708203
	cr[1] = {2825393, 1182141, 171, 239, 61}
	aN[353][2][1] = 1708203
	dN = nil
	aY[1] = nil
	ch = nil
	cB = true
	ci[1] = "IsLoaded"
	bg = "IsLoaded"
	local dN
	aN[353][3][1] = 1708203
	dN = {2825393, 1182141, 171, 239, 61}
	cr[1] = nil
	ct[1] = {2825393, 1182141, 171, 239, 61}
	dN = 1
	co[1] = {159, 95, 54, 82, 224, 105, 212, 191}
	cl = 1
	dN = nil
	cm[1] = nil
	cj[1] = nil
	cB = true
	ci[1] = ""
	co[1] = {20, 142, 40, 163, 108, 19, 127, 78, 123, 236, 153, 168, 33, 186, 211, 152, 180, 142, 32, 158, 42, 134, 105, 195, 211, 175, 253, 152, 172, 146, 208, 175, 27, 210, 186, 12, 135, 127, 241, 204, 78, 98, 129, 224, 246, 47, 123, 38, 87, 94, 79, 71, 126, 61, 131, 80, 74, 180, 6, 93, 199, 98, 23, 53}
	ct[1] = {340661, 2847643, 55, 119, 39}
	aN[353][3][1] = 6267158
	cl = 1
	cB = true
	ci[1] = "2ab80ae141b17f8e8ec6266171048dbacc255535afb6c3b7e25180eaea6d1be1"
	bd = "2ab80ae141b17f8e8ec6266171048dbacc255535afb6c3b7e25180eaea6d1be1"
	cB = true
	ci[1] = ""
	aN[353][3][1] = 10321302
	co[1] = {41, 176, 235, 59, 76, 172, 114}
	ct[1] = {1555645, 3966379, 147, 161, 189}
	cj[1] = 1
	cB = true
	ci[1] = "getfenv"
	bE = "getfenv"
	cB = true
	cs = 1
	aN[353][3][1] = 8183864
	cm[1] = {3938021, 3283243, 69, 115, 111}
	cj[1] = ""
	ct[1] = {}
	local dN
	dN = nil
	co[1] = 8183864
	aN[353][3][1] = nil
	cr[1] = nil
	cB = true
	cj[1] = ""
	bb = ""
	cB = true
	while aN[67]do aN[1060]=aN[72];end
	co[1] = 13832690
	cm[1] = {1298177, 2526807, 133, 129, 197}
	cs = 1
	cj[1] = ""
	ct[1] = {13, 213, 22, 35, 124, 100, 92}
	cB = true
	cj[1] = "getgenv"
	bF = "getgenv"
	cB = true
	cp = 1
	co[1] = 12601160
	aV[1] = {76, 76, 112, 12, 169, 44, 180, 18, 116, 92, 39, 119, 100, 201, 59, 72, 233, 115, 229, 31, 89, 22, 225, 8, 15, 61, 152, 84, 244, 66, 157, 124, 114, 192, 60, 99, 9, 152, 215, 31, 46, 101, 127, 95, 91, 27, 32, 47, 159, 73, 113, 62, 225, 204, 223, 163, 105, 125, 95, 107, 207, 234, 131, 18, 64, 206, 240, 168, 249, 96, 159, 131, 156, 114, 196, 207, 224, 130, 73, 148, 96, 140, 228, 180, 148, 18, 254, 220, 161, 248, 0, 98, 139, 116, 109, 56, 62, 101, 91, 189, 67, 242, 227, 231, 210, 145, 190, 10, 41, 95, 116, 61, 246, 57, 111, 96, 165, 20, 31, 84, 180, 118, 205, 99, 169, 41, 75, 227, 150, 151, 4, 26, 127, 178, 98, 74, 50, 240, 126, 185, 94, 21, 77, 176, 86, 188, 80, 81, 236, 95, 106, 151, 183, 170, 27, 241, 94, 46, 229, 134, 156, 127, 113, 48, 61, 139, 189, 13, 170, 123, 220, 195, 132, 68, 125, 146, 120, 247, 106, 216, 23, 136, 253, 191, 236, 197, 184, 92, 243, 228, 209, 115, 176, 171, 172, 75, 199, 52, 212, 2, 147, 49, 52, 180, 226, 66, 195, 100, 83, 82, 69, 173, 223, 240, 97, 18, 94, 255, 124, 146, 127, 50, 55, 147, 243, 200, 170, 68, 199, 119, 225, 83, 8, 126, 241, 46, 56, 33, 111, 209, 188, 61, 101, 96, 87, 42, 34, 68, 199, 2, 134, 104, 181, 8, 153, 25, 8, 93, 209, 17, 102, 136, 55, 48, 117, 242, 110, 142, 201, 132, 221, 141, 116, 1, 136, 55, 27, 155, 190, 1, 188, 97, 232, 88, 32, 217, 119, 77, 150, 93, 7, 186, 83, 224, 83, 82, 94, 110, 144, 121, 114, 123, 9, 216, 207, 172, 26, 121, 76, 64, 141, 117, 232, 237, 24, 50, 232, 95, 144, 216, 192, 111, 112, 62, 39, 243, 200, 83, 36, 92, 99, 82, 231, 101, 12, 194, 238, 182, 117, 35, 127, 50, 188, 226, 204, 248, 39, 252, 193, 114, 53, 66, 161, 246, 23, 206, 169, 90, 49, 238, 254, 136, 230, 218, 110, 90, 103, 241, 133, 7, 159, 253, 30, 56, 65, 63, 23, 32, 225, 77, 234, 246, 246, 184}
	cr[1] = ""
	cm[1] = {790653, 835007, 21, 35, 197}
	local dN
	dN = nil
	aN[353][3][1] = nil
	aN[353][1][1] = nil
	cB = true
	cr[1] = "Polsec is a Lua whitelisting service, and attempting to deobfuscate, reverse-engineer, or otherwise bypass its protections is against the service’s Terms of Service. Continuing to do so could potentially get the owner or other involved parties in trouble, including account or service consequences. Stop attempting to deobfuscate or bypass Polsec and leave the protected code alone."
	bp = "Polsec is a Lua whitelisting service, and attempting to deobfuscate, reverse-engineer, or otherwise bypass its protections is against the service’s Terms of Service. Continuing to do so could potentially get the owner or other involved parties in trouble, including account or service consequences. Stop attempting to deobfuscate or bypass Polsec and leave the protected code alone."
	cB = true
	co[1] = 14341035
	aV[1] = {252, 217, 2, 90}
	cp = 1
	cr[1] = ""
	aY[1] = {3189345, 435517, 153, 187, 75}
	cB = true
	cr[1] = "game"
	bC = "game"
	local dN
	dN = nil
	cj[1] = nil
	cm[1] = nil
	dN = nil
	ch = nil
	aU[1] = nil
	cB = true
	cr[1] = ""
	aY[1] = {1995225, 1763503, 209, 43, 169}
	cp = 1
	cq[1] = {228, 113, 84, 245, 116, 156}
	co[1] = 14302181
	cB = true
	cr[1] = "Loaded"
	bj = "Loaded"
	local dN
	cl = nil
	cj[1] = "Loaded"
	dN = nil
	ch = nil
	aW[1] = nil
	cB = true
	aY[1] = {1866561, 3542541, 229, 193, 127}
	cj[1] = ""
	cq[1] = 1
	co[1] = 10901877
	cp = {73, 88, 145, 29, 13}
	cB = true
	cj[1] = "trial"
	bT = "trial"
	local dN
	cr[1] = {1866561, 3542541, 229, 193, 127}
	aY[1] = nil
	dN = nil
	ct[1] = nil
	aW[1] = nil
	cB = true
	cr[1] = {2524105, 2525395, 221, 131, 5}
	cq[1] = 1
	aN[353][4][1] = {49, 130, 131, 98, 87, 92, 126, 28, 218, 70, 201, 255}
	co[1] = 6600152
	cj[1] = ""
	cB = true
	cm[1] = "getmetatable"
	bG = "getmetatable"
	local dN
	dN = {49, 130, 131, 98, 87, 92, 126, 28, 218, 70, 201, 255}
	aN[353][4][1] = "getmetatable"
	cm[1] = {49, 130, 131, 98, 87, 92, 126, 28, 218, 70, 201, 255}
	dN = nil
	aW[1] = {2524105, 2525395, 221, 131, 5}
	cr[1] = nil
	cB = true
	aN[353][4][1] = ""
	cq[1] = 1
	cm[1] = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
	aW[1] = {1870621, 1612495, 101, 87, 73}
	co[1] = 15956315
	local dN
	dN = nil
	aV[1] = 15956315
	co[1] = nil
	dN = nil
	ci[1] = nil
	cr[1] = nil
	aN[353][1][1] = nil
	cB = true
	aN[353][4][1] = "script_key"
	bP = "script_key"
	cB = true
	repeat if bo==nil then aW[1]={((cA+4304793)-(cA+322308)),((cA+3227513)-(cA+579326)),((cA+502800)-(cA+502675)),((cA+308396)-(cA+308387)),((cA+101698)-(cA+101511))};aN[353][3][1]=1;aV[1]=((cA+7993948)-(cA+909868));cm[1]={186,3,254,211,98,214};aN[353][1][1]='';end;cA=(483+cA);cA=(4233+cA);do local dN;cp=aW[1];aW[1]=cm[1];dN=aN[353][1][1];aN[353][1][1]=cf;cf=dN;end;cB=true;cC,dC=836529+cA,(cA-322)+(58151+322);dJ=cC;until aN[161]
	local dN
	co[1] = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
	cm[1] = nil
	dN = "script_key"
	aN[353][1][1] = nil
	aN[353][2][1] = 1
	aN[353][3][1] = {73, 88, 145, 29, 13}
	cp = nil
	ch = nil
	cr[1] = {1870621, 1612495, 101, 87, 73}
	aW[1] = "script_key"
	dN = nil
	ct[1] = nil
	cx[1] = nil
	cB = true
	aN[144] = nil
	aN[236] = nil
	aN[211] = nil
	aV[1] = nil
	cB = true
	cB = true
	cq[1] = aN[144][bG]
	aX[1] = aN[144][bu]
	cu[1] = (if aN[72]==404587 then cq[1]else aN[367])(aX[1])
	cs = not cu[1]
	local dN
	aY[1] = nil
	cj[1] = 1
	aN[353][1][1] = nil
	aN[353][2][1] = nil
	ci[1] = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
	cm[1] = cq[1]
	dN = nil
	cr[1] = nil
	cf = cs
	cs = nil
	cB = true
	cu[1] = "Loaded"
	ck[1] = aX[1][(if aN[72]==404587 then cu[1]else aN[383])]
	cl = nil
	cq[1] = nil
	cg[1] = nil
	local es,et=ck[1],cg[1]
	cn[1] = es[et]
	local eu=(if aN[67]then aN[374]else cn[1])
	aW[1] = eu(ck[1])
	local dN
	ch = cf
	cs = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
	dN = nil
	cx[1] = 1
	cj[1] = nil
	dN = nil
	aN[353][2][1] = nil
	aU[1] = nil
	cB = true
	ck[1] = "2ab80ae141b17f8e8ec6266171048dbacc255535afb6c3b7e25180eaea6d1be1"
	cu[1] = "2ab80ae141b17f8e8ec6266171048dbacc255535afb6c3b7e25180eaea6d1be1"
	cg[1] = nil
	ck[1] = nil
	cl = "Polsec is a Lua whitelisting service, and attempting to deobfuscate, reverse-engineer, or otherwise bypass its protections is against the service’s Terms of Service. Continuing to do so could potentially get the owner or other involved parties in trouble, including account or service consequences. Stop attempting to deobfuscate or bypass Polsec and leave the protected code alone."
	local dN
	cf = cm[1]
	dN = nil
	aN[353][2][1] = "Polsec is a Lua whitelisting service, and attempting to deobfuscate, reverse-engineer, or otherwise bypass its protections is against the service’s Terms of Service. Continuing to do so could potentially get the owner or other involved parties in trouble, including account or service consequences. Stop attempting to deobfuscate or bypass Polsec and leave the protected code alone."
	cl = nil
	cB = true
	local dN
	aY[1] = nil
	aN[353][4][1] = nil
	cj[1] = "Polsec is a Lua whitelisting service, and attempting to deobfuscate, reverse-engineer, or otherwise bypass its protections is against the service’s Terms of Service. Continuing to do so could potentially get the owner or other involved parties in trouble, including account or service consequences. Stop attempting to deobfuscate or bypass Polsec and leave the protected code alone."
	aN[353][2][1] = nil
	aN[353][1][1] = ch
	ch = nil
	dN = nil
	cp = nil
	cr[1] = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
	ci[1] = cm[1]
	cm[1] = nil
	dN = cf
	cf = {160, 134, 70, 179, 222, 60, 230, 61, 119, 190}
	cs = dN
	cB = true
	cf = ce(aW[1],cp,aV[1])
	bo = cf
	local dN
	cm[1] = nil
	dN = nil
	aN[353][4][1] = nil
	cl = nil
	cB = true
	aN[353][3][1] = 1
	aW[1] = {242, 62, 55, 250}
	cf = ""
	cp = {856189, 665721, 31, 125, 215}
	aV[1] = 1263479
	local dN
	aN[353][2][1] = nil
	dN = aN[353][1][1]
	aN[353][1][1] = ""
	cf = dN
	dN = 1263479
	aV[1] = 1
	aN[353][3][1] = 1263479
	dN = nil
	aY[1] = ci[1]
	ci[1] = nil
	cB = true
	local dN
	ch = cf
	cs = nil
	aN[353][2][1] = nil
	aU[1] = {242, 62, 55, 250}
	aW[1] = nil
	dN = "Polsec is a Lua whitelisting service, and attempting to deobfuscate, reverse-engineer, or otherwise bypass its protections is against the service’s Terms of Service. Continuing to do so could potentially get the owner or other involved parties in trouble, including account or service consequences. Stop attempting to deobfuscate or bypass Polsec and leave the protected code alone."
	cj[1] = 1
	cx[1] = "Polsec is a Lua whitelisting service, and attempting to deobfuscate, reverse-engineer, or otherwise bypass its protections is against the service’s Terms of Service. Continuing to do so could potentially get the owner or other involved parties in trouble, including account or service consequences. Stop attempting to deobfuscate or bypass Polsec and leave the protected code alone."
	cB = true
	ci[1] = not cp
	local ev=ci[1]
	cB = true
	cu[1] = "trial"
	aX[1] = "trial"
	aN[144][bP]=aX[1]
	local dN
	cq[1] = nil
	dN = nil
	cl = {242, 62, 55, 250}
	aU[1] = nil
	cB = true
	cB = true
	cu[1] = aN[144][bC]
	aX[1] = cu[1]
	cu[1] = nil
	cu[1] = "IsLoaded"
	ck[1] = aX[1][cu[1]]
	local ew=ck[1]
	cg[1] = ew(aX[1])
	cn[1] = not cg[1]
	if cn[1] then
	cA = 1766700
	ci[1],cr[1],cj[1],co[1]=cp,cj[1],cr[1],aN[353][1][1]
	cB = true
	cC = 2834468
	dC = 1857575
	dJ = 1885471
	else
	cA = 1764741
	do local dN;ci[1]=cp;co[1]=cf;cf=aN[353][1][1];dN=cj[1];cj[1]=aY[1];aY[1]=cr[1];cr[1]=dN;end
	cB = true
	cC = 2730798
	dC = 1853447
	dJ = 1885471
	end
	cB = true
	aN[353][1][1] = ce(aW[1],cp,aN[353][3][1])
	bV = aN[353][1][1]
	local dN
	dN = nil
	aN[353][2][1] = nil
	cm[1] = 1
	aN[353][4][1] = nil
	dN = 1
	ct[1] = nil
	aY[1] = 1
	cB = true
	cf = cc(aW[1],cp,aN[353][3][1])
	be = cf
	cB = true
	cq[1] = {216, 99, 43, 188}
	cf = ""
	cp = {813493, 2363849, 91, 209, 183}
	cm[1] = 1
	aN[353][3][1] = 12872556
	local dN
	dN = nil
	aN[353][2][1] = nil
	aN[353][4][1] = 1
	aY[1] = nil
	cB = true
	cf = "Wait"
	bs = "Wait"
	cB = true
	aU[1] = aN[144][bE]
	cq[1] = nil
	aX[1] = (if not aN[67]then aU[1]else aN[370])(cq[1])
	cs = "print"
	aV[1] = "print"
	cu[1] = "print"
	ck[1] = aX[1][cu[1]]
	cg[1] = nil
	aW[1] = (if aN[72]==404587 then cg[1]else aN[416])==(if aN[72]==404587 then ck[1]else aN[366])
	cn[1] = true
	aY[1] = true
	local ex=aY[1]
	cB = true
	local dN
	cx[1] = nil
	ct[1] = aW[1]
	aW[1] = {216, 99, 43, 188}
	aN[353][1][1] = {813493, 2363849, 91, 209, 183}
	cp = 12872556
	cs = true
	dN = "Wait"
	cf = 1
	aU[1] = "Wait"
	dN = "print"
	aV[1] = cl
	cl = "print"
	cB = true
	cq[1] = nil
	cq[1] = nil
	cn[1] = nil
	cg[1] = nil
	aW[1] = aN[144][bF]
	cf = aW[1]()
	cr[1] = bo
	cf[cr[1]]=cg[1]
	cn[1] = (function(ey,ez,eA,eB)return function(...)return(function(...)
	-- for-dispatch over eC=540..806 step 7
	aH = 0
	aH = 0
	aN = {}
	aH = 1342
	aN[568+159]=568~=750
	aM = true
	aN[(751+6)-6]=582+9585
	aN[(589-589)+664]=589+7758
	aN[(596-596)+802]=596+6728
	aN[603+179]=603+6192
	aN[604] = 3804
	aN[617+225]=617+1534
	aN[817] = true
	aN[787] = true
	aN[(638-638)+733]=638+8811
	aN[645+154]=645+430
	aN[(726+337)-337]=652+3451
	aN[(659-659)+636]=659+2969
	aN[(666-666)+721]=666+3688
	aN[(680-680)+713]=680+6215
	aN[85] = 631730
	aN[694+63]=694+7452
	aN[(750+47)-47]=701~=771
	aN[708-678]=not false
	aN[715-492]=715~=715
	aN[722+116]=722+5340
	aN[(729-729)+878]=729+5623
	aN[(680+385)-385]=736+8986
	aN[743+155]=743+2667
	aN[750-58]=750+4910
	aN[(814+105)-105]=757+1892
	aN[764+41]=764+4887
	aN[878] = 10466
	aN[(778+107)-107]=778+6606
	aN[605] = true
	aQ = function(...)
	aN[534][18][1] = fy
	co[1] = fz
	aX[1] = fA
	cu[1] = fB
	dC[1] = fC
	if(fF-fD)<=1476976 then if 845345>(fF-fD)then if 421578<(fF-fD)then if not((fF-fD)<555022)then if(fF-fD)<650825 then if(fF-fD)~=555023 then if not((fG-fD)~=84380)then if aN[85]==631730 then if eF==nil then cr[1]={54,116};aN[534][8][1]={((fD+2086580)-(fD+861211)),((fD+43951)-(fD+11268)),((fD+983510)-(fD+983427)),((fD+54714)-(fD+54573)),((fD+752525)-(fD+752448))};aV='';aN[534][1][1]=((fD+7832191)-(fD+6779));aN[534][7][1]=1;end;fD=fD+6018;fD=(fD+9566);fr[1],ft[1],cp[1]=cp[1],cg,fr[1];fE=true;fF=845345+fD;fG=(fD-229)+(61227+229);fJ=fF;else aN[1060]=aN[85];end;end end else if(fF-fD)>650825 then if 674802<=(fF-fD)then if not((fF-fD)>=740313)then if(fF-fD)~=674803 then if not((fG-fD)<=66027 or(fG-fD)>=66928)then while aN[223]do aN[905]=aN[85];end;fD=7257+fD;do local dN;ft[1]=aU[1];aU[1]=fr[1];dN=ct[1];ct[1]=aN[534][23][1];aN[534][23][1]=dN;end;fE=true;fF,fG=674802+fD,1202+fD;fJ=fF;elseif not(1202~=(fG-fD))then fD=(fD+5436);do local dN;dN=cp[1];cp[1]=aN[534][21][1];aN[534][21][1]=dN;end;fE=true;fF=674802+fD;fG=fD+56552;fJ=fF;elseif not(56552~=(fG-fD))then dG[1]=bB;ci[1]=(if aN[30]then dL[1]else aN[575])[(if not aN[30]then aN[542]else dG[1])];cl[1]=(if aN[85]~=631730 then aN[593]else aN[565]);cl[1]=(if aN[85]~=631730 then aN[534]else bv);aN[534][22][1]=(if aN[223]then aN[538]else ci[1])[(if aN[85]==631730 then cl[1]else aN[545])];fD=(15679+fD);aN[534][10][1]=(if aN[30]then bB else aN[588]);fD=(4547+fD);aN[534][23][1]=(if aN[85]==631730 then dL[1]else aN[555])[(if aN[30]then aN[534][10][1]else aN[596])];aN[534][13][1]=bw;ft[1]=aN[534][13][1];local fL,fM=aN[534][23][1],ft[1];aN[534][15][1]=fL[fM];fD=fD+19575;cj[1],fs[1]=aN[534][22][1],aN[534][14][1](aN[534][15][1]);fD=9965+fD;ci[1]=function(...)local fN=function(...)
	-- for-dispatch over fO=840..1144 step 8
	aN = {}
	aN[848-155]=848~=1048
	aH = 1373
	aM = true
	aN[(834+115)-115]=872+6289
	aN[670] = true
	aN[(888-888)+691]=888+4765
	aN[731] = true
	aN[61] = true
	aN[912-102]=912+6849
	aN[688] = 3307
	aN[(928-928)+632]=928+283
	aN[(936-936)+683]=936+268
	aN[944-195]=944+2424
	aN[952-272]=952+5894
	aN[(643+272)-272]=960+7161
	aN[968-94]=968+8907
	aN[(681+305)-305]=976+8169
	aN[984-222]=984~=1040
	aN[992-129]=992+8035
	aN[1000-393]=1000~=1056
	aN[(1008-1008)+738]=1008+2779
	aN[45] = false
	aN[713] = 1835
	aN[886] = 3035
	aN[(1040-1040)+846]=1040+5176
	aN[(1048-1048)+805]=1048+2204
	aN[1056-408]=1056+155
	aN[1064-462]=1064+1845
	aN[(672+217)-217]=1072+9189
	aN[1080-442]=1080~=928
	aN[(1088-1088)+891]=1088+6009
	aN[738] = 9895
	aN[1104-452]=1104+1974
	aN[(662+94)-94]=1112~=1040
	aN[(1120-1120)+193]=536186
	aX = function(...)
	-- PARSE ERROR: PARSE_ERROR: expected name None got '1128' @314
	aI = aX
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @37194
	return fN(aN[534][11],fu,fv,cs,cj,aN[534][14],aN[534][6],aW,aN[534][5],fw,aN[534][4],aN[534][2],dG,aX,dJ,aY,fx,dL,aN[534][18],ck,aN[534][17],aN[534][12],cu,dC,aN[534][9],cm,co,fs,cC,cx,dE,aN[534][16],...)end
	fD = 266647
	cg = ci[1]
	fD = 270882
	fD = 270704
	do local dN;cA=aV;cf=aU[1];aU[1]=cg;cg=cr[1];end
	fE = true
	fF,fG=674802+fD,fD+84477
	fJ = 582328
	elseif(fG-fD)<84726 and 84396<(fG-fD)then dG[1]=aU[1]
	fD = 269227
	ci[1] = nil
	cl[1] = aN[54][bR]
	aN[534][22][1] = nil
	aN[534][10][1] = (if aN[85]~=631730 then aN[540]else cl[1])[(if aN[85]==631730 then aN[534][22][1]else aN[595])]
	aN[534][23][1] = 5
	local gx=ci[1]
	ft[1] = gx(aN[534][10][1],aN[534][23][1],dG[1])
	fD = 287934
	cl[1] = {}
	fD = 267878
	aN[534][22][1] = nil
	fD = 273094
	aN[534][10][1] = false
	cl[1][aN[534][22][1]]=aN[534][10][1]
	fD = 271077
	aN[534][13][1] = nil
	aN[534][22][1],aN[534][10][1]=aN[534][13][1],aN[223]
	cl[1][aN[534][22][1]]=(if aN[85]~=631730 then aN[569]else aN[534][10][1])
	ci[1] = nil
	fD = 301848
	aN[534][22][1] = function(...)local gy=function(...)
	-- for-dispatch over gz=946..1016 step 2
	aH = 0
	aN = {}
	aN[950-248]=950+8964
	aN[952-218]=952+5655
	aH = 1580
	aN[956-331]=956+2631
	aM = true
	aN[(860+364)-364]=960+1306
	aN[(624+466)-466]=962~=974
	aN[(767+380)-380]=964+5702
	aN[966-751]=true
	aN[(897+89)-89]=968+6694
	aN[620] = true
	aN[652] = 8633
	aN[(674+410)-410]=974+5066
	aN[976-247]=976+2058
	aN[978-301]=978+1443
	aN[980-317]=980+1125
	aN[(982-982)+702]=982+4686
	aN[984-108]=984+715
	aN[986-301]=986+3261
	aN[(674+196)-196]=988+5877
	aN[990-352]=990+5659
	aN[992-381]=992+3608
	aN[(994-994)+618]=994~=1012
	aN[996-347]=996+883
	aN[998-300]=998~=980
	aN[(1000-1000)+803]=1000+9656
	aN[706] = 3002
	aN[43] = false
	aN[788] = 3027
	aN[1008-956]=112633
	aN[(762+84)-84]=1010+3095
	aW = function(...)
	fr[1] = gE
	dC[1] = gF
	aN[355][4][1] = gG
	return cx
	ft = ce(ck[1],aN[355][2][1],cm)
	eW = ft
	local dN
	cs = nil
	cC[1] = nil
	dN = nil
	aU = nil
	dE[1] = nil
	fE = true
	fG = 616469
	cf[1] = 1
	cm = 2225760
	aN[355][2][1] = {1562193, 2891029, 59, 41, 219}
	ck[1] = {244, 180, 166}
	ft = ""
	local dN
	dJ[1] = nil
	dC[1] = nil
	dN = nil
	cg = 1
	cf[1] = nil
	dN = 12872556
	aV[1] = nil
	cx = 12872556
	fE = true
	fF,fG=fD+759276,5353+fD
	cu[1] = (if aN[52]~=112633 then aN[397]else(378755+(-378750)))
	cr = (if co[1]==cu[1]then aN[215]else not aN[215])
	cA[1] = cr
	local dN
	aW = nil
	dG[1] = 1
	dN = nil
	ci = {244, 180, 166}
	ck[1] = nil
	dN = nil
	fr[1] = 12872556
	cx = nil
	dN = nil
	dL[1] = nil
	cl[1] = nil
	fE = true
	fG = 641808
	cn = cA[1]
	fr[1] = not cA[1]
	if not fr[1] then
	fD = 2146491
	do local dN;aV[1]=cf[1];dN=aY[1];aY[1]=aN[355][9][1];aN[355][9][1]=fr[1];fr[1]=dC[1];dC[1]=dN;dN=dJ[1];dJ[1]=ch;ch=dN;dN=cr;cr=cp;cp=dN;dN=cm;cm=cn;cn=dN;end
	fE = true
	fF = 2989619
	fG = 2189824
	fJ = 2745317
	else
	fD = 2139952
	do local dN;aV[1]=cf[1];dN=cp;cp=cr;cr=dN;end
	fE = true
	fF,fG=850310+fD,(fD-985)+(13588+985)
	fJ = 2745317
	end
	dC[1] = fA[1]
	aN[355][7][1] = eW
	local dN
	aW = nil
	cA[1] = nil
	fr[1] = {813493, 2363849, 91, 209, 183}
	cj[1] = nil
	cs = aN[355][7][1]
	dN = co[1]
	co[1] = nil
	fs[1] = dN
	dN = nil
	aV[1] = nil
	ct[1] = nil
	fE = true
	fG = 639965
	aV[1] = cs
	fs[1] = aV[1]
	local gH,gI=cg,fs[1]
	aN[355][8][1] = gH[gI]
	cp = (if aN[43]then aN[373]else dC[1])(aN[355][8][1])
	fE = true
	fG = 643878
	dC[1] = nil
	fs[1] = cg[(if not aN[215]then aN[381]else dC[1])]
	aN[355][8][1] = 200
	local dN
	aN[355][7][1] = aN[355][6][1]
	dN = {813493, 2363849, 91, 209, 183}
	fr[1] = 1
	aN[355][9][1] = {813493, 2363849, 91, 209, 183}
	fE = true
	fG = 678971
	cn = aN[355][8][1]~=fs[1]
	cp = (if aN[43]then aN[386]else not cn)
	aV[1] = cp
	ct[1] = nil
	ct[1] = nil
	if cp then
	fD = 2141437
	dL[1],ck[1],cq[1]=cn,cq[1],ck[1]
	fE = true
	fF,fG=(fD-661)+(478386+661),38147+fD
	fJ = 2745317
	else
	fD = 2149298
	cx,dL[1],cm,cr,dJ[1],cs,dG[1],ci,ck[1],ch,aN[355][9][1],cq[1]=ci,cn,cu[1],ch,cx,aN[355][9][1],cq[1],dJ[1],dG[1],cr,cs,ck[1]
	fE = true
	fF = 3795956
	fG = 2161894
	fJ = 2745317
	end
	aU = (if aN[52]==112633 then aN else aN[396])
	aU = {}
	aX[1] = nil
	local dN
	cm = nil
	dN = nil
	cs = {813493, 2363849, 91, 209, 183}
	aN[355][9][1] = nil
	dN = nil
	dG[1] = nil
	ck[1] = nil
	dN = nil
	cx = nil
	dJ[1] = nil
	fE = true
	fF,fG=652616+fD,(fD-804)+(75622+804)
	while aN[43]do aN[945]=aN[52];end
	if bb==nil then
	ft = bZ(cg,aN[355][2][1],cm)
	bb = 1
	end
	fE = true
	fG = 678328
	local dN
	dN = 1
	fr[1] = aN[355][6][1]
	aN[355][6][1] = 1
	dN = nil
	cm = nil
	dG[1] = nil
	fE = true
	fF,fG=fD+1549681,fD+94113
	aU = fB[1]
	dG[1] = gi[1]
	aX[1] = aU(dG[1])
	cC[1] = eW
	dE[1][cC[1]]=(if aN[43]then aN else aX[1])
	aW = nil
	local dN
	ck[1] = nil
	dJ[1] = nil
	cx = nil
	dE[1] = fr[1]
	fr[1] = fs[1]
	dN = nil
	aW = nil
	aN[355][9][1] = nil
	dN = aN[355][7][1]
	aN[355][7][1] = aX[1]
	aX[1] = dN
	fE = true
	fF,fG=1549681+fD,(fD-963)+(71286+963)
	local dN
	cp = nil
	co[1] = dL[1]
	fs[1] = ch
	cu[1] = cl[1]
	cl[1] = aV[1]
	aV[1] = ft
	ft = 1
	aN[355][6][1] = nil
	dL[1] = nil
	ch = nil
	cx = nil
	aW = aU
	aU = nil
	dC[1] = dG[1]
	dG[1] = {813493, 2363849, 91, 209, 183}
	cs = nil
	cm = nil
	cr = {244, 180, 166}
	ct[1] = nil
	dN = dE[1]
	dE[1] = nil
	cA[1] = cq[1]
	cq[1] = 200
	aN[355][8][1] = aN[355][7][1]
	aN[355][7][1] = aX[1]
	aX[1] = dN
	fE = true
	fF,fG=(fD-574)+(1644363+574),80650+fD
	local dN
	cp = co[1]
	co[1] = nil
	aU = 1
	ft = nil
	aN[355][6][1] = {813493, 2363849, 91, 209, 183}
	fs[1] = nil
	fE = true
	fG = 756053
	co[1] = getfenv[fm]
	ci = nil
	aN[355][6][1] = nil
	cC[1] = co[1][aN[355][6][1]]
	ci = nil
	ck[1] = (if aN[52]~=112633 then aN else aN[382])
	ck[1] = nil
	cs = nil
	ch = cx[(if aN[52]==112633 then cs else aN[370])]
	aN[355][7][1] = cC[1](ch)
	ci = nil
	ck[1] = nil
	ck[1] = nil
	cq[1] = nil
	local gJ,gK,gL=cx,cq[1],aN[355][7][1]
	gJ[gK]=gL
	co[1] = 4
	cn = nil
	cn = {}
	aN[355][6][1] = (if cn then aN[43]else not aN[43])
	cC[1] = nil
	fs[1] = (if aN[355][6][1]then aN[43]else aN[215])
	local gM=fs[1]
	fE = true
	fF,fG=(if gM then fD+442638 else fD+442638),(if gM then(fD-827)+(24581+827)else fD+24024)
	fr[1] = ""
	aN[355][2][1] = {2117041, 3923149, 111, 173, 61}
	cf[1] = 1
	cl[1] = 5618367
	ck[1] = {251, 249, 101, 159, 170, 150, 136, 79}
	local dN
	aN[355][9][1] = nil
	dN = fs[1]
	fs[1] = cA[1]
	cA[1] = dN
	dN = {}
	aX[1] = cj[1]
	cj[1] = {}
	fE = true
	fF,fG=fD+1572531,(fD-634)+(70289+634)
	fr[1] = "authSent"
	eS = "authSent"
	fE = true
	fF,fG=fD+1572531,fD+88748
	if bj==nil then
	ft = ""
	aN[355][2][1] = {1574817, 631475, 89, 71, 177}
	ck[1] = {35, 209, 32, 229, 131, 75, 205}
	cl[1] = 10183188
	cf[1] = 1
	end
	local dN
	aW = nil
	cr = fs[1]
	dN = cu[1]
	cu[1] = cA[1]
	cA[1] = 4
	co[1] = dN
	dN = nil
	aY[1] = nil
	dJ[1] = nil
	fE = true
	fF,fG=(fD-218)+(1572531+218),46813+fD
	if bj==nil then
	ft = cc(ck[1],aN[355][2][1],cl[1])
	bj = 1
	end
	local dN
	fs[1] = nil
	dN = cr
	cr = nil
	dG[1] = dN
	fE = true
	fG = 873715
	repeat if eW==nil then ft='';ck[1]={195};cl[1]=((fD+6657163)-(fD+707514));cf[1]=1;aN[355][2][1]={((fD+193145)-(fD+31680)),((fD+1854804)-(fD+742501)),((fD+25298)-(fD+25141)),((fD+654746)-(fD+654673)),((fD+596700)-(fD+596665))};end;fD=4626+fD;fD=(7964+fD);cl[1],cr,aN[355][7][1],aW,cn,cC[1],cm=cm,cC[1],cn,dC[1],aN[355][7][1],cr,cl[1];fE=true;fF=(fD-844)+(1306931+844);fG=8724+fD;fJ=fF;until aN[215]
	fr[1] = getfenv[bV]
	aX[1] = eW
	cf[1] = cg[(if aN[52]~=112633 then aN[360]else aX[1])]
	aN[355][3][1] = (if aN[43]then aN else fr[1])(cf[1])
	ck[1] = "string"
	cn = aN[355][3][1]~=ck[1]
	aN[355][9][1] = not cn
	cx = aN[355][9][1]
	cA[1] = (if aN[52]==112633 then cx else aN[375])
	fE = true
	fF,fG=fD+1724493,(fD-300)+(78914+300)
	cx = nil
	dE[1] = nil
	local gN=aU
	fE = true
	fF,fG=(if gN then fD+1724493 else 1724493+fD),(if gN then fD+57466 else 23639+fD)
	cj[1] = eW
	dJ[1] = cj[1]
	local gO,gP=cg,dJ[1]
	cq[1] = gO[gP]
	aN[355][6][1] = (if aN[52]==112633 then aN else aN[418])
	aN[355][6][1] = {}
	local dN
	ck[1] = 1
	dN = nil
	ct[1] = nil
	cx = nil
	dN = {}
	aN[355][6][1] = cu[1]
	cu[1] = {}
	fE = true
	fG = 1002930
	dG[1] = cu[1]~=cq[1]
	dE[1] = nil
	local dN
	dN = cj[1]
	cj[1] = {}
	aN[355][7][1] = dN
	dN = aV[1]
	aV[1] = aU
	aU = "string"
	fr[1] = dN
	fE = true
	fG = 993944
	aY[1] = true
	local gQ=aY[1]
	fE = true
	fF,fG=(if gQ then 478386+fD else fD+478386),(if gQ then fD+19102 else(fD-898)+(30686+898))
	ft = cc(cg,aN[355][2][1],cm)
	eY = ft
	fE = true
	fF,fG=(fD-660)+(128151+660),(fD-709)+(26178+709)
	if bb==nil then
	cm = 8523568
	ft = ""
	aN[355][2][1] = {987729, 2820755, 159, 175, 239}
	cn = 1
	cg = {}
	end
	local dN
	dN = 1
	ck[1] = aV[1]
	aV[1] = 1
	dN = cp
	cp = nil
	dJ[1] = dN
	fE = true
	fG = 1032088
	fr[1] = bZ(dJ[1],aN[355][2][1],aU)
	fm = fr[1]
	local dN
	dN = nil
	fs[1] = nil
	dE[1] = nil
	fE = true
	fF,fG=fD+1538542,(fD-747)+(78659+747)
	ct[1] = 1
	fr[1] = ""
	dJ[1] = {140, 218, 105, 110, 211, 155, 218, 168}
	aN[355][2][1] = {618489, 682927, 177, 91, 203}
	aU = 10323688
	local dN
	dG[1] = aX[1]
	cj[1] = 1
	dN = ft
	ft = nil
	dE[1] = dN
	fE = true
	fG = 1089518
	fr[1] = "tonumber"
	fo = "tonumber"
	fE = true
	fG = 1107151
	if bV==nil then
	fr[1] = ""
	ct[1] = 1
	dJ[1] = {197, 52, 7, 27}
	aU = 2272481
	aN[355][2][1] = {2147033, 786993, 75, 123, 199}
	end
	fE = true
	fG = 1095485
	if bV==nil then
	fr[1] = bZ(cl[1],aN[355][2][1],aU)
	bV = fr[1]
	end
	fE = true
	fF,fG=935919+fD,fD+26652
	co[1] = 8
	local gR=cn
	cq[1] = gR(cp,co[1])
	local dN
	cu[1] = "tonumber"
	dN = aN[355][6][1]
	aN[355][6][1] = {140, 218, 105, 110, 211, 155, 218, 168}
	cl[1] = dN
	dN = 1
	ct[1] = nil
	aW = 1
	fE = true
	fF,fG=59130+fD,fD+48383
	aN[355][3][1] = (if aN[52]==112633 then fs[1]..cq[1]else aN[358])
	local gS=ch
	cA[1] = gS(aN[355][3][1])
	fE = true
	fF,fG=(fD-245)+(59130+245),93706+fD
	aN[1037] = aN[52]+173
	fE = true
	fG = 1132612
	fE = true
	fF,fG=1003775+fD,fD+18382
	if aN[52]==112633 then
	fD = 2144283
	do local dN;cs=cq[1];aW=cl[1];cl[1]=dL[1];aY[1]=cx;cx=aV[1];end
	fE = true
	fF = 3863802
	fG = 2202600
	fJ = 2745317
	else
	aN[954] = nil
	end
	local dN
	cp = dJ[1]
	dN = nil
	cC[1] = 8
	aW = nil
	dN = 1
	aV[1] = 1
	cx = 1
	fE = true
	fG = 1161288
	ct[1] = aN[52]==112633
	cp = {}
	cp = (if aN[43]then aN else ct[1])
	aU = cp
	cl[1] = aU
	cA[1] = fC[1]
	cu[1] = "authSent"
	fE = true
	fF,fG=fD+1900942,fD+80751
	cA[1][cu[1]]=(if aN[215]then cl[1]else aN[369])
	local dN
	cC[1] = "authSent"
	cq[1] = 1
	cx = nil
	dN = cl[1]
	cl[1] = nil
	aW = dN
	dN = 1
	ck[1] = 8
	cf[1] = 1
	fE = true
	fF,fG=1900942+fD,(fD-52)+(78344+52)
	fE = true
	fG = 1205932
	if aN[52]==112633 then
	fD = 2141574
	dE[1],cn,co[1],ch,dG[1],fr[1],dC[1],dL[1],cm,fs[1],aN[355][7][1],cl[1],aN[355][6][1]=dG[1],cl[1],aN[355][7][1],cm,ch,aN[355][6][1],dE[1],cx,dC[1],fr[1],co[1],cn,fs[1]
	fE = true
	fF,fG=fD+1549681,fD+94113
	fJ = 2745317
	else
	aN[1083] = nil
	end
	aU = true
	aX[1] = true
	cm = nil
	cC[1] = eY
	local gT,gU,gV=cm,cC[1],aX[1]
	gT[gU]=gV
	local dN
	dN = aN[355][7][1]
	aN[355][7][1] = co[1]
	co[1] = dN
	dN = cl[1]
	cl[1] = nil
	cn = dN
	dN = fs[1]
	fs[1] = {}
	fr[1] = dN
	fE = true
	fG = 1215968
	aV[1] = {}
	ft = {}
	if not ct[1] then
	fD = 2148182
	do local dN;aN[355][6][1]=cx;cn=cg;cg=cl[1];aY[1]=cp;dN=aV[1];aV[1]=cj[1];cj[1]=dN;dN=fr[1];fr[1]=aN[355][8][1];aN[355][8][1]=dJ[1];dJ[1]=dN;dN=co[1];co[1]=aX[1];aX[1]=dN;dN=ft;ft=aW;aW=dN;end
	fE = true
	fF = 3795956
	fG = 2174693
	fJ = 2745317
	else
	fD = 2144332
	do local dN;cn=cg;cg=cl[1];end
	fE = true
	fF,fG=(fD-377)+(124139+377),fD+54736
	fJ = 2745317
	end
	ch = nil
	dG[1] = cn[(if aN[52]==112633 then ch else aN[404])]
	cm = nil
	local gW,gX=dG[1],cm
	dJ[1] = gW[gX]
	cj[1] = 1
	aN[355][9][1] = 7
	fE = true
	fG = 1243127
	aV[1] = (if aN[52]~=112633 then aN[355]else aN[409])
	aV[1] = nil
	ci = nil
	local gY=aN[355][8][1]
	aN[355][1][1] = gY(dG[1],cj[1],ci)
	aN[355][9][1] = "Loaded"
	aV[1] = "Loaded"
	aX[1] = "Loaded"
	dL[1] = aN[355][1][1]~=aX[1]
	cs = (if dL[1]then aN[52]~=112633 else aN[215])
	ft = {}
	ft = (if aN[52]==112633 then cs else aN)
	fE = true
	fG = 1311521
	cg = not aW
	local gZ=cg
	fE = true
	fF,fG=(if gZ then(fD-435)+(124139+435)else(fD-992)+(976379+992)),(if gZ then fD+96380 else fD+95056)
	local dN
	ck[1] = "Loaded"
	cu[1] = 1
	aN[355][9][1] = cn
	cn = true
	aU = 1
	cl[1] = nil
	aN[355][6][1] = true
	cq[1] = 10323688
	cr = nil
	ct[1] = aW
	aW = true
	aY[1] = cA[1]
	cA[1] = ft
	ft = nil
	ch = dC[1]
	dN = aN[355][7][1]
	aN[355][7][1] = cs
	cs = dN
	dN = nil
	cm = cg
	cg = dG[1]
	dG[1] = nil
	ci = nil
	dN = dJ[1]
	dJ[1] = 1
	cf[1] = aN[355][8][1]
	aN[355][8][1] = dN
	fE = true
	fG = 1336554
	aN[355][2][1] = {1752877, 2450947, 233, 193, 175}
	cg = {112, 178, 92, 10, 88}
	cu[1] = 1
	fs[1] = ""
	cm = 10261396
	fE = true
	fF,fG=1311546+fD,(fD-623)+(1062+623)
	aN[968] = aN[52]+261
	fs[1] = "clone"
	gB = "clone"
	fE = true
	fF,fG=fD+1311546,(fD-859)+(65713+859)
	aN[355][2][1] = {1056865, 3900281, 223, 247, 93}
	fs[1] = ""
	cm = 4635483
	cg = {162}
	cu[1] = 1
	local dN
	dC[1] = 8
	dN = 1
	aV[1] = 10323688
	cn = cs
	cs = 1
	dN = dE[1]
	dE[1] = 1
	cu[1] = dN
	fE = true
	fG = 1331474
	fs[1] = "d"
	bz = "d"
	fE = true
	fG = 1356432
	dL[1] = 4
	dG[1] = dL[1]~=co[1]
	cf[1] = nil
	cf[1] = nil
	cA[1] = nil
	aU = true
	fE = true
	fF,fG=fD+1044996,fD+44654
	dG[1] = 3
	cC[1] = nil
	cC[1] = (if aN[52]==112633 then dG[1]else aN[409])
	fE = true
	fG = 1398697
	cm = cC[1]
	ch = cm
	fs[1] = (if cC[1]then not aN[215]else aN[52]==112633)
	if not fs[1] then
	fD = 2141839
	ch,fs[1],aW,cl[1],aN[355][8][1],cq[1],cm,aN[355][6][1],dL[1]=cx,ch,aN[355][6][1],fs[1],cq[1],aN[355][8][1],dL[1],aW,cm
	fE = true
	fF = 2581947
	fG = 2233690
	fJ = 2745317
	else
	fD = 2142278
	aW,aN[355][8][1],cq[1],cm,aN[355][6][1],dL[1]=aN[355][6][1],cq[1],aN[355][8][1],dL[1],aW,cm
	fE = true
	fF,fG=fD+442638,(fD-526)+(89412+526)
	fJ = 2745317
	end
	local dN
	cl[1] = fs[1]
	fs[1] = ch
	ch = true
	dN = ci
	ci = 1
	aN[355][8][1] = dN
	fE = true
	fG = 1456588
	local dN
	dN = aN[355][8][1]
	aN[355][8][1] = 1
	ci = dN
	dN = true
	aU = nil
	aW = true
	fE = true
	fG = 1454249
	aV[1] = ct[1]
	ft = aV[1]
	local ha=ct[1]
	if nil then
	do local dN;cn=cg;cg=cl[1];end
	else
	do local dN;aN[355][6][1]=cx;aY[1]=cp;cn=cg;cg=cl[1];dN=aX[1];aX[1]=co[1];co[1]=dN;dN=aV[1];aV[1]=cj[1];cj[1]=dN;dN=aW;aW=ft;ft=dN;dN=aN[355][8][1];aN[355][8][1]=dJ[1];dJ[1]=fr[1];fr[1]=dN;end
	end
	fE = true
	fF,fG=(if ha then(fD-698)+(124139+698)else fD+1656647),(if ha then 54736+fD else 35384+fD)
	ch = nil
	local hb,hc=cn,ch
	dG[1] = hb[hc]
	cm = nil
	dJ[1] = dG[1][(if aN[43]then aN[383]else cm)]
	fE = true
	fF,fG=124139+fD,fD+28103
	repeat aV[1]=aN[355][9][1];ci=aV[1];local hd=aN[355][8][1];aN[355][1][1]=hd(dG[1],cj[1],ci);aN[355][9][1]=bj;aV[1]=(if aN[43]then aN[373]else aN[355][9][1]);aX[1]=aV[1];fD=(fD+35358);dL[1]=(if aN[43]then aN[361]else aN[355][1][1]~=aX[1]);cs=not dL[1];fD=6418+fD;ft=cs;fD=fD+2281;fD=6322+fD;ft,aY[1],aV[1],cj[1],aW=aW,cp,cj[1],aV[1],ft;fE=true;fF,fG=(fD-274)+(1656647+274),(fD-260)+(35384+260);fJ=fF;until aN[215]
	cg = nil
	if cg then
	fD = 2139483
	cp,aW,cx,aY[1],cs,cl[1]=aY[1],cs,ck[1],aN[355][9][1],aW,cq[1]
	fE = true
	fF = 2263448
	fG = 2235689
	fJ = 2745317
	else
	fD = 2143345
	ct[1],ft,cp,aN[355][9][1],aW,cx,cr,aY[1],cs,cl[1]=ft,cr,aY[1],cg,cs,ck[1],ct[1],aN[355][9][1],aW,cq[1]
	fE = true
	fF,fG=(fD-522)+(976379+522),(fD-907)+(95056+907)
	fJ = 2745317
	end
	local dN
	cq[1] = nil
	cr = ct[1]
	ct[1] = 1
	cu[1] = cl[1]
	aN[355][9][1] = {162}
	aW = "Loaded"
	cl[1] = true
	aN[355][6][1] = 1
	ck[1] = 7
	aY[1] = nil
	cA[1] = ft
	ft = nil
	ch = 8
	cn = nil
	aU = aV[1]
	dN = dG[1]
	dG[1] = ci
	ci = nil
	cm = nil
	cg = dN
	dN = aN[355][8][1]
	aN[355][8][1] = dJ[1]
	dJ[1] = nil
	cf[1] = dN
	dN = true
	cs = aN[355][7][1]
	aN[355][7][1] = true
	fE = true
	fF,fG=fD+59130,43449+fD
	if aN[52]==112633 then
	fD = 2139454
	do local dN;cn=aX[1];aX[1]=ci;dN=dC[1];dC[1]=aU;aU=dN;end
	fE = true
	fF,fG=1644363+fD,80650+fD
	fJ = 2745317
	else
	aN[916] = nil
	end
	dC[1] = fx[1]
	cC[1] = fy[1]
	dG[1] = fC[1]
	aW = dC[1](cC[1],cl[1],ch,aN[355][4][1],dG[1])
	dC[1] = 5
	cC[1] = dC[1]==cl[1]
	dL[1] = cC[1]
	dG[1] = nil
	dG[1] = nil
	local he=cC[1]
	fE = true
	fF,fG=(if he then(fD-522)+(1644363+522)else 1644363+fD),(if he then fD+92426 else(fD-162)+(46458+162))
	local dN
	dL[1] = nil
	ck[1] = cp
	cp = fs[1]
	ch = cC[1]
	cj[1] = 1
	dN = cg
	cg = cs
	cs = dN
	fE = true
	fF,fG=(fD-741)+(1572723+741),(fD-651)+(55980+651)
	fE = true
	fF,fG=(fD-10)+(1572723+10),fD+9159
	local hf,hg=cg,aX[1]
	ch = hf[hg]
	aN[355][3][1] = (if aN[215]then aU else aN)(ch)
	cA[1] = "string"
	dL[1] = cA[1]~=aN[355][3][1]
	fr[1] = not dL[1]
	aV[1] = fr[1]
	ct[1] = nil
	fE = true
	fF,fG=fD+1656647,fD+22585
	cp = getfenv[bV]
	cA[1] = (if aN[215]then cp else aN[379])(ci)
	fr[1] = fm
	cn = (if aN[52]==112633 then aN[404]else aN[385])
	cn = (if aN[43]then aN[412]else fr[1]~=cA[1])
	cf[1] = not cn
	dL[1] = cf[1]
	fE = true
	fG = 1601597
	cx = (if aN[355][8][1]then aN[43]else aN[52]==112633)
	if cx then
	fD = 2140940
	do local dN;aX[1]=aN[355][7][1];ct[1]=cj[1];cj[1]=cC[1];cC[1]=aV[1];dN=cl[1];cl[1]=dL[1];dL[1]=dN;dN=cf[1];cf[1]=ck[1];ck[1]=dN;end
	fE = true
	fF,fG=(fD-105)+(901170+105),90401+fD
	fJ = 2745317
	else
	fD = 2142651
	dL[1],cl[1],aN[355][7][1],aX[1],ck[1],cf[1],cs,ct[1],cj[1],dE[1],aU,cC[1]=cl[1],aU,aY[1],aN[355][7][1],cs,ck[1],cf[1],cj[1],cC[1],aV[1],dL[1],dE[1]
	fE = true
	fF = 3040479
	fG = 2234676
	fJ = 2745317
	end
	repeat dE[1]=1;fD=4517+fD;fs[1]=dE[1];fD=fD+7182;fD=7214+fD;aU,aW=aW,aU;fE=true;fF=(fD-121)+(684124+121);fG=(fD-870)+(54631+870);fJ=fF;until aN[215]
	aN[355][7][1] = fs[1]
	aU = fB[1]
	cC[1] = getfenv[fo]
	cs = nil
	dG[1] = nil
	local dN
	cx = nil
	dN = true
	aX[1] = aV[1]
	aV[1] = true
	fE = true
	fF,fG=684124+fD,(fD-391)+(60824+391)
	local hh,hi=ch,dG[1]
	fs[1] = hh[hi]
	dE[1] = (if aN[43]then aN[360]else fs[1])[(if not aN[215]then aN[396]else aN[355][7][1])]
	co[1] = aU(cC[1](dE[1]))
	fr[1] = (if aN[52]==112633 then aN[407]else aN[361])
	fr[1] = (if aN[52]~=112633 then aN[390]else bw)
	cf[1] = ch[fr[1]]
	(if not aN[43]then cf[1]else aN)[(if not aN[43]then aN[355][7][1]else aN)]=co[1]
	local dN
	cA[1] = dE[1]
	ck[1] = 8
	dN = aW
	aW = nil
	cm = 1
	dJ[1] = dN
	dN = cr
	cr = nil
	cs = dN
	fE = true
	fF,fG=684124+fD,fD+83807
	local dN
	dE[1] = 8
	cl[1] = aX[1]
	aX[1] = true
	aV[1] = dJ[1]
	dN = co[1]
	co[1] = nil
	aW = dN
	dN = 1
	ct[1] = 1
	aN[355][6][1] = 1
	fE = true
	fF,fG=1644363+fD,fD+2958
	cg = {208, 52, 103, 58, 179, 170, 241, 101}
	fs[1] = ""
	cm = 3834820
	aN[355][2][1] = {3519969, 1468393, 125, 213, 217}
	cn = 1
	local dN
	aN[355][6][1] = cj[1]
	cu[1] = 1
	dN = nil
	cx = aV[1]
	aV[1] = nil
	fE = true
	fG = 1729197
	fs[1] = "Banned: "
	gA = "Banned: "
	local dN
	cn = cs
	cf[1] = 5
	dN = aN[355][6][1]
	aN[355][6][1] = 1
	ct[1] = dN
	fE = true
	fF,fG=(fD-800)+(1311546+800),33165+fD
	cu[1] = 5
	cr = co[1]==cu[1]
	cA[1] = (if aN[43]then aN else cr)
	fE = true
	fG = 1789386
	cn = cA[1]
	fr[1] = (if aN[52]~=112633 then aN else aN[383])
	fr[1] = (if aN[52]==112633 then not cA[1]else aN)
	if not fr[1] then
	fD = 2148082
	do local dN;aV[1]=cf[1];dN=cp;cp=cr;cr=dN;dN=dJ[1];dJ[1]=ch;ch=dN;dN=fr[1];fr[1]=dC[1];dC[1]=aY[1];aY[1]=aN[355][9][1];aN[355][9][1]=dN;dN=cm;cm=cn;cn=dN;end
	fE = true
	fF = 2989619
	fG = 2189824
	fJ = 2745317
	else
	fD = 2147485
	do local dN;aV[1]=cf[1];dN=cp;cp=cr;cr=dN;end
	fE = true
	fF,fG=fD+850310,fD+13588
	fJ = 2745317
	end
	cp = cl[1]~=aN[355][8][1]
	aV[1] = (if aN[43]then aN[396]else cp)
	cA[1] = aV[1]
	cx = not cp
	if cx then
	fD = 2140533
	cg,cr,ci=ci,cm,cg
	fE = true
	fF,fG=606008+fD,57380+fD
	fJ = 2745317
	else
	fD = 2141277
	do local dN;cr=cm;dG[1]=cs;dN=ci;ci=cg;cg=dN;dN=aN[355][7][1];aN[355][7][1]=fs[1];fs[1]=dN;end
	fE = true
	fF,fG=76914+fD,19112+fD
	fJ = 2745317
	end
	fE = true
	fG = 1826349
	ft = cb(ck[1],aN[355][2][1],cm)
	fl = ft
	local dN
	cA[1] = cf[1]
	dN = fs[1]
	fs[1] = nil
	cs = dN
	dN = ct[1]
	ct[1] = 5
	cu[1] = dN
	fE = true
	fG = 1772794
	if eY==nil then
	cm = 8004799
	cg = 1
	aN[355][2][1] = {3633329, 1756585, 137, 213, 209}
	ck[1] = {146, 168, 166}
	ft = ""
	end
	local dN
	aN[355][9][1] = 3834820
	cr = cu[1]
	dN = true
	aX[1] = nil
	co[1] = true
	dN = cn
	cn = 8
	cg = 10323688
	ck[1] = dN
	fE = true
	fG = 1844214
	aN[67] = getfenv
	aN[172] = string
	aN[211] = string.char
	fE = true
	fF,fG=fD+794416,47336+fD
	aN[110] = "format"
	aN[37] = string[aN[110]]
	local dN
	cf[1] = dG[1]
	cC[1] = true
	dN = 10323688
	cg = cm
	cm = dL[1]
	dL[1] = 10323688
	dN = 8
	cn = aY[1]
	aY[1] = 8
	fE = true
	fF,fG=794416+fD,81711+fD
	if fm==nil then
	aU = 6634097
	dJ[1] = {199, 149, 90, 200, 79}
	ct[1] = 1
	aN[355][2][1] = {3219745, 210623, 239, 135, 83}
	fr[1] = ""
	end
	fE = true
	fF,fG=(fD-88)+(1538542+88),(fD-145)+(69840+145)
	ci = 20
	aX[1] = 20
	cl[1] = aX[1]~=aV[1]
	aU = not cl[1]
	local hj=aU
	if nil then
	do local dN;dN=cq[1];cq[1]=aN[355][6][1];aN[355][6][1]=dN;end
	else
	cg,aN[355][7][1],ch,aN[355][6][1],cs,cq[1],cA[1]=ck[1],cs,cA[1],cq[1],aN[355][7][1],aN[355][6][1],ch
	end
	fE = true
	fF,fG=(if hj then fD+1262686 else fD+1931532),(if hj then fD+76001 else 82808+fD)
	aN[953] = aN[52]+370
	fE = true
	fF,fG=(fD-437)+(1931532+437),fD+71998
	if eS==nil then
	ck[1] = {251, 249, 101, 159, 170, 150, 136, 79}
	cf[1] = 1
	cl[1] = 5618367
	aN[355][2][1] = {2117041, 3923149, 111, 173, 61}
	fr[1] = ""
	end
	fE = true
	fF,fG=1572531+fD,70289+fD
	if eS==nil then
	fr[1] = ce(ck[1],aN[355][2][1],cl[1])
	eS = fr[1]
	end
	local dN
	ft = fr[1]
	fr[1] = cr
	ci = aN[355][9][1]
	dN = cm
	cm = cn
	cn = dN
	fE = true
	fG = 1943568
	if bj==nil then
	cf[1] = 1
	ft = ""
	cl[1] = 10183188
	aN[355][2][1] = {1574817, 631475, 89, 71, 177}
	ck[1] = {35, 209, 32, 229, 131, 75, 205}
	end
	fE = true
	fF,fG=(fD-236)+(1572531+236),fD+46813
	if bj==nil then
	ft = cc(ck[1],aN[355][2][1],cl[1])
	bj = 1
	end
	local dN
	fs[1] = aW
	dN = 5
	cr = 5
	dG[1] = 5
	fE = true
	fG = 1882912
	if eW==nil then
	ft = ""
	cf[1] = 1
	aN[355][2][1] = {161465, 1112303, 157, 73, 35}
	cl[1] = 5949649
	ck[1] = {195}
	end
	local dN
	aW = 8
	dN = true
	cC[1] = 5
	cr = true
	dN = cn
	cn = aN[355][7][1]
	aN[355][7][1] = dN
	dN = cl[1]
	cl[1] = cm
	cm = dN
	fE = true
	fG = 1897859
	aN[355][6][1] = (if aN[52]==112633 then(346189+(-346180))else aN)
	aX[1] = co[1]>=aN[355][6][1]
	ck[1] = aX[1]
	local hk=aX[1]
	fE = true
	fF,fG=(if hk then 850310+fD else(fD-763)+(850310+763)),(if hk then(fD-288)+(21357+288)else(fD-497)+(20686+497))
	ct[1] = 14
	ch = 14
	cs = 14
	aN[355][3][1] = co[1]<=cs
	ck[1] = aN[355][3][1]
	local dN
	dN = 14
	ch = dJ[1]
	dJ[1] = 14
	fE = true
	fG = 1966383
	dJ[1] = ck[1]
	cm = dJ[1]
	local dN
	dN = 8
	dC[1] = {208, 52, 103, 58, 179, 170, 241, 101}
	aY[1] = aN[355][9][1]
	aN[355][9][1] = fr[1]
	fr[1] = 8
	fE = true
	fF,fG=(fD-158)+(850310+158),50515+fD
	fr[1] = cm
	aN[355][9][1] = not fr[1]
	local hl=aN[355][9][1]
	fE = true
	fF,fG=(if hl then fD+850310 else(fD-96)+(1900942+96)),(if hl then 30925+fD else 60860+fD)
	repeat fD=4258+fD;do local dN;cj[1]=co[1];co[1]=cg;cq[1]=aU;cf[1]=ck[1];ck[1]=aW;aW=aN[355][9][1];aN[355][9][1]=fr[1];fr[1]=aX[1];aX[1]=cl[1];cl[1]=cC[1];cC[1]=cu[1];cu[1]=dJ[1];aU=aV[1];aV[1]=cx;cx=dL[1];dN=ci;ci=ct[1];ct[1]=dN;end;fE=true;fF=(fD-207)+(1262686+207);fG=fD+44425;fJ=fF;until aN[215]
	if bQ==nil then
	cl[1] = {160, 46, 177, 50, 39, 178}
	ck[1] = 242108
	aN[355][2][1] = {2067205, 2381575, 55, 249, 103}
	fr[1] = ""
	cf[1] = 1
	end
	fE = true
	fG = 1996715
	if bQ==nil then
	fr[1] = bZ(ck[1],aN[355][2][1],cl[1])
	bQ = fr[1]
	end
	fE = true
	fG = 2050531
	while aN[43]do aN[968]=aN[52];end
	fE = true
	fF,fG=fD+976379,fD+31483
	dC[1] = fA[1]
	fs[1] = (if aN[52]~=112633 then aN[409]else gA)
	dG[1] = nil
	cj[1] = nil
	fr[1] = nil
	fE = true
	fF,fG=fD+976379,63731+fD
	local hm,hn=aU,fr[1]
	cp = hm[hn]
	cr = nil
	cn = (if aN[52]==112633 then cp else aN[382])[(if aN[43]then aN[355]else cr)]
	local dN
	aY[1] = aN[355][7][1]
	aN[355][7][1] = 14
	ch = dC[1]
	dN = aV[1]
	aV[1] = aU
	aU = dN
	fE = true
	fG = 2096834
	aN[355][2][1] = {2180577, 181443, 181, 195, 233}
	aU = 10649480
	fr[1] = ""
	ct[1] = 1
	cl[1] = {219}
	fE = true
	fF,fG=935919+fD,(fD-685)+(69818+685)
	fr[1] = "e"
	bB = "e"
	fE = true
	fF,fG=935919+fD,(fD-108)+(46721+108)
	aN[355][9][1] = 1
	cl[1] = {186}
	ck[1] = 5147011
	fr[1] = ""
	aN[355][2][1] = {1863297, 1689907, 107, 145, 43}
	fE = true
	fF,fG=935919+fD,(fD-771)+(29855+771)
	if aN[52]==112633 then
	if bw==nil then fr[1]=cc(cl[1],aN[355][2][1],ck[1]);bw=fr[1];end
	fD = 2144106
	fD = 2147938
	do local dN;dN=ct[1];ct[1]=cA[1];cA[1]=dN;dN=cm;cm=cq[1];cq[1]=dN;dN=cr;cr=fs[1];fs[1]=dN;end
	fE = true
	fF = 3615013
	fG = 2180388
	fJ = 2745317
	else
	aN[960] = nil
	end
	local dN
	cr = true
	cA[1] = dL[1]
	dL[1] = cn
	cn = ""
	fr[1] = cm
	cm = cx
	cx = ci
	ci = dJ[1]
	aN[355][7][1] = cC[1]
	dJ[1] = aX[1]
	aX[1] = ct[1]
	ct[1] = ch
	ch = dC[1]
	dC[1] = 8
	aN[355][6][1] = {186}
	cl[1] = 1
	aN[355][9][1] = aY[1]
	aY[1] = 14
	cs = nil
	cu[1] = aN[355][8][1]
	aN[355][8][1] = nil
	cq[1] = 1
	cf[1] = 5147011
	ck[1] = nil
	cj[1] = aW
	aW = nil
	fs[1] = 5
	aU = nil
	dE[1] = 14
	ft = 1
	cg = co[1]
	fE = true
	fG = 2119559
	fE = true
	fG = 2135293
	dC[1] = nil
	dC[1] = nil
	cl[1] = ci[(if not aN[43]then dC[1]else aN)]
	aN[355][8][1] = 200
	fE = true
	fG = 2196786
	-- region end
	-- warn: no leaf for key (582328, 794416)
	-- warn: repeat-until 'aN[215]' not pre-true; one-shot assumed
	-- warn: repeat-until 'aN[215]' not pre-true; one-shot assumed
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @40878
	aL = aW
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @43077
	return gy(aN[534][11],fu,fv,cs,cj,aN[534][14],aN[534][6],aW,ci,aN[534][5],fw,aN[534][4],aN[534][2],dG,aX,dJ,aY,fx,dL,aN[534][18],ck,aN[534][17],aN[534][12],cu,dC,aN[534][9],cm,co,cl,fs,cC,cx,dE,aN[534][16],...)end
	aU[1] = nil
	fD = 281505
	cl[1] = "Wait"
	aN[534][22][1] = nil
	aN[534][22][1] = (if aN[223]then aN[590]else aN[54][fo])
	fD = 274500
	fD = 268845
	do local dN;dN=ft[1];ft[1]=aN[534][21][1];aN[534][21][1]=dN;dN=cn;cn=aN[534][20][1];aN[534][20][1]=dN;dN=aN[534][23][1];aN[534][23][1]=aN[534][22][1];aN[534][22][1]=dN;end
	fE = true
	fF,fG=(fD-445)+(1180144+445),(fD-878)+(54082+878)
	fJ = 582328
	end end else
	-- sub-region (fF,fG) base fD:
	aN[534][1][1] = 2235916
	cr[1] = {55}
	aV = ""
	aN[534][7][1] = 1
	aN[534][8][1] = {974173, 3252123, 169, 45, 79}
	local dN
	dN = nil
	cn = nil
	cp[1] = nil
	aN[534][22][1] = ""
	aV = nil
	fE = true
	aN[534][22][1] = "e"
	bB = "e"
	local dN
	dN = nil
	aN[534][20][1] = nil
	ft[1] = "Wait"
	aU[1] = nil
	ch[1] = nil
	fE = true
	aN[534][7][1] = 1
	aN[534][8][1] = {3022485, 1647287, 17, 55, 81}
	cr[1] = {212, 185, 152, 221}
	aN[534][1][1] = 214665
	aN[534][22][1] = ""
	fE = true
	aN[534][22][1] = "http"
	bI = "http"
	fE = true
	aN[534][7][1] = 1
	aN[534][1][1] = 16403415
	cr[1] = {45, 170, 255, 254, 103, 228, 203, 87}
	aN[534][8][1] = {3957681, 3608887, 159, 63, 15}
	aN[534][22][1] = ""
	fE = true
	aN[534][3][1] = nil
	cj[1] = ""
	fs[1] = aX[1]..cj[1]
	ch[1][aN[534][3][1]]=fs[1]
	aN[534][3][1] = nil
	aN[534][3][1] = nil
	(if not aN[223]then ch[1]else aN[570])[(if aN[85]==631730 then aN[534][3][1]else aN[553])]=cu[1]
	dL[1],aN[534][16][1]=cs[1](cA,aN[534][21][1],ch[1])
	cA = true
	aU[1] = false
	fE = true
	while aN[223]do aN[998]=aN[85];end
	fE = true
	cA = nil
	ct[1] = nil
	ct[1] = false
	aN[534][22][1] = true
	cn = true
	ch[1] = {}
	local dN
	fr[1] = nil
	dN = nil
	cA = false
	ct[1] = nil
	dN = true
	cn = nil
	aN[534][20][1] = true
	fE = true
	-- sub-region (fF,fG) base fD:
	cr[1] = true
	local dN
	cf = nil
	cq[1] = nil
	dN = nil
	cn = nil
	ch[1] = nil
	dN = nil
	cg = true
	cr[1] = nil
	fE = true
	aN[1051] = 632373
	fE = true
	while aN[223]do aN[901]=aN[85];end
	fE = true
	aN[534][13][1] = nil
	cl[1] = nil
	ci[1] = nil
	local dN
	dN = nil
	aV = nil
	cr[1] = nil
	fE = true
	-- sub-region (fF,fG) base fD:
	aN[534][21][1] = bZ(aN[534][23][1],aN[534][8][1],aN[534][1][1])
	fn = aN[534][21][1]
	fE = true
	-- sub-region (fF,fG) base fD:
	cl[1] = (if aN[85]==631730 then ch[1]else aN)+dL[1]
	cA = cl[1]
	dL[1] = cA
	fE = true
	aN[54] = getfenv
	aN[82] = string
	aN[111] = string.char
	fE = true
	aN[138] = "format"
	aN[176] = string[aN[138]]
	fE = true
	aN[534][1][1] = 6738535
	aV = {139, 155, 11, 5}
	cq[1] = ""
	aN[534][8][1] = {858733, 396331, 57, 57, 153}
	aN[534][7][1] = 1
	fE = true
	cq[1] = "last"
	fc = "last"
	local dN
	aN[534][23][1] = nil
	dN = nil
	cA = "last"
	cq[1] = nil
	dN = nil
	cp[1] = nil
	ft[1] = fr[1]
	fr[1] = nil
	fE = true
	aV = {65, 42, 141, 166, 232}
	cA = ""
	aN[534][7][1] = 1
	aN[534][8][1] = {1638753, 1237989, 205, 31, 167}
	aN[534][1][1] = 7037273
	fE = true
	cl[1] = 0
	aN[534][20][1] = (if aN[85]==631730 then(if cl[1]<aN[534][11][1]then aN[30]else aN[223])else aN[543])
	aN[534][10][1] = nil
	aN[534][10][1] = (if aN[85]~=631730 then aN[572]else aN[534][20][1])
	cq[1] = not aN[534][20][1]
	ft[1] = 500
	aN[534][22][1] = (if not aN[30]then aN[548]else aN[534][11][1])<ft[1]
	aN[534][10][1] = nil
	aN[534][10][1] = nil
	fE = true
	if nil then
	fD = 471950
	do local dN;aN[534][21][1]=cA;dN=aN[534][22][1];aN[534][22][1]=cp[1];cp[1]=dN;end
	fE = true
	fF = 966292
	fG = 550319
	fJ = 884826
	else
	fD = 472452
	do local dN;aN[534][23][1]=cf;cg=cA;aN[534][21][1]=fr[1];cf=cr[1];fr[1]=cn;cn=aN[534][22][1];cr[1]=ch[1];ch[1]=ft[1];ft[1]=cp[1];cA=cq[1];dN=aN[534][20][1];aN[534][20][1]=aV;aV=dN;end
	fE = true
	fF = 1555737
	fG = 552107
	fJ = 884826
	end
	local dN
	aN[534][23][1] = cr[1]
	dN = nil
	ch[1] = 500
	ft[1] = nil
	aN[534][22][1] = nil
	fE = true
	cq[1] = cb(aN[534][23][1],aN[534][8][1],aN[534][1][1])
	bA = cq[1]
	fE = true
	aN[534][23][1] = {114, 235, 118, 227, 156}
	aN[534][1][1] = 15396450
	aN[534][8][1] = {3732981, 2995079, 187, 41, 169}
	aN[534][7][1] = 1
	cn = ""
	fE = true
	cf = "setup"
	fj = "setup"
	local dN
	dN = aN[534][21][1]
	aN[534][21][1] = "setup"
	cf = dN
	fE = true
	aN[534][7][1] = 1
	aN[534][23][1] = {142, 47, 32, 7, 159, 61, 105, 123}
	aN[534][1][1] = 10011079
	aN[534][8][1] = {3146713, 2336353, 133, 139, 239}
	aN[534][21][1] = ""
	local dN
	dN = {65, 42, 141, 166, 232}
	aU[1] = nil
	cp[1] = {65, 42, 141, 166, 232}
	dN = nil
	cq[1] = ch[1]
	ch[1] = nil
	fE = true
	aU[1] = bZ(aN[534][21][1],aN[534][8][1],aN[534][1][1])
	bJ = aU[1]
	fE = true
	repeat if bv==nil then aU[1]='';aN[534][8][1]={((fD+698778)-(fD+111429)),((fD+2348627)-(fD+97622)),((fD+498179)-(fD+498124)),((fD+963819)-(fD+963790)),((fD+686249)-(fD+686068))};aN[534][21][1]={196};aN[534][7][1]=1;aN[534][1][1]=((fD+2065870)-(fD+657435));end;fD=fD+8187;fD=(fD+3884);do local dN;aN[534][20][1]=ft[1];dN=cA;cA=fr[1];fr[1]=dN;dN=cn;cn=cp[1];cp[1]=dN;dN=aN[534][21][1];aN[534][21][1]=ct[1];ct[1]=dN;end;fE=true;fF=fD+495041;fG=(fD-783)+(87766+783);fJ=fF;until aN[30]
	aN[997] = 632482
	aU[1] = cb(ct[1],aN[534][8][1],aN[534][1][1])
	bv = aU[1]
	fE = true
	while aN[223]do aN[1036]=aN[85];end
	aN[534][1][1] = 14056625
	ct[1] = {142, 53, 253, 76, 23, 75, 33, 178, 71, 190}
	aN[534][7][1] = 1
	aN[534][23][1] = ""
	aN[534][8][1] = {1149329, 1663475, 177, 85, 39}
	fE = true
	if 240753>(fF-fD)then if(fF-fD)<=66184 then if not((fF-fD)>44093)then if(fF-fD)~=44094 then if 18884==(fG-fD)then repeat aN[534][23][1]=aN[54][bV];aN[534][10][1]=aN[534][23][1](cu[1]);ft[1]=bQ;fD=(fD+13197);ch[1]=aN[534][10][1]==ft[1];cl[1]=ch[1];fD=16442+fD;fD=8866+fD;cq[1],aV,cA=aV,cA,cq[1];fE=true;fF,fG=66184+fD,4889+fD;fJ=fF;until aN[30];end end else if 66184<=(fF-fD)then if not((fG-fD)<=4816 or(fG-fD)>=5365)then aN[534][15][1]=cl[1];fD=(fD+8437);if cl[1]then fD=fD+5478;do local dN;cp[1]=aN[534][22][1];fr[1]=aV;aV=aU[1];dN=cq[1];cq[1]=cr[1];cr[1]=ft[1];ft[1]=dN;end;fE=true;fF=fD+66184;fG=(fD-368)+(44162+368);fJ=fF;else fD=(fD+4637);ft[1],cr[1],aV,ch[1],fr[1],cq[1],cn,cp[1]=ch[1],ft[1],aU[1],cq[1],aV,cr[1],cg,aN[534][22][1];fE=true;fF=1029361+fD;fG=(fD-289)+(45635+289);fJ=fF;end;elseif not((fG-fD)~=44162)then aN[948]=aN[85]+614;fD=(fD+9808);do local dN;cn=cg;dN=fr[1];fr[1]=cq[1];cq[1]=dN;dN=ft[1];ft[1]=ch[1];ch[1]=dN;dN=cf;cf=cA;cA=dN;end;fE=true;fF,fG=1152002+fD,95341+fD;fJ=fF;end end end else if 134304>(fF-fD)then if(fF-fD)~=109227 then if 42227==(fG-fD)then fD=(fD+9197);aN[534][21][1],ft[1],cn,cg,cq[1],cf=aN[534][23][1],cg,aN[534][20][1],ft[1],cr[1],aN[534][21][1];fE=true;fF,fG=109226+fD,fD+8769;fJ=fF;elseif 8769==(fG-fD)then repeat aN[534][13][1]=0;cA=aN[534][13][1];aN[534][13][1]=1;cg=(if aN[30]then aN[534][13][1]else aN[536]);fD=(16957+fD);ch[1]={};aN[534][13][1]=bv;fD=(fD+7012);aN[534][3][1]=aN[534][13][1];ch[1][aN[534][3][1]]=aN[534][18][1];fD=fD+12263;fD=(fD+7811);cg,aN[534][21][1]=aN[534][21][1],cg;fE=true;fF=(fD-962)+(109226+962);fG=35718+fD;fJ=fF;until aN[30];elseif not((fG-fD)>=35726)and 35443<(fG-fD)then while aN[223]do aN[1012]=aN[85];end;aN[534][13][1]=(if aN[30]then aN else aN);aN[534][13][1]=(if aN[85]~=631730 then aN[559]else bw);aN[534][3][1]=aN[534][13][1];fD=7401+fD;ch[1][aN[534][3][1]]=(if aN[223]then aN[544]else co[1]);fD=(5907+fD);fD=(fD+9685);ct[1],cn=cn,ct[1];fE=true;fF=fD+821743;fG=(fD-858)+(61526+858);fJ=fF;end end else if(fF-fD)<236055 then if(fF-fD)~=134305 then if(fG-fD)==12696 then if not cj[1]then fD=(5895+fD);do local dN;cp[1]=aV;dN=ft[1];ft[1]=aN[534][23][1];aN[534][23][1]=ch[1];ch[1]=dN;dN=aN[534][21][1];aN[534][21][1]=aN[534][20][1];aN[534][20][1]=ct[1];ct[1]=aN[534][22][1];aN[534][22][1]=dN;end;fE=true;fF,fG=fD+421578,(fD-672)+(70343+672);fJ=fF;else fD=7899+fD;do local dN;dN=ch[1];ch[1]=ft[1];ft[1]=dN;dN=aN[534][20][1];aN[534][20][1]=ct[1];ct[1]=aN[534][21][1];aN[534][21][1]=dN;end;fE=true;fF,fG=134304+fD,97932+fD;fJ=fF;end;elseif 97932==(fG-fD)then aN[534][13][1]=(if aN[85]==631730 then eM else aN[584]);fD=2779+fD;dL[1]=aN[534][13][1];fD=(4132+fD);aN[534][13][1]=eQ;aN[534][16][1]=(if not aN[223]then aN[534][13][1]else aN);cA=(if aN[85]~=631730 then aN[544]else aN[534][9][1])(dL[1],aN[534][16][1]);dL[1]=aN[54][fq];aN[534][16][1]=eL;fD=23728+fD;cA=(if aN[30]then dL[1]else aN[573])(aN[534][16][1]);fD=fD+2068;return;end end else if(fF-fD)>=236055 then if(fG-fD)==83446 then cg,cr[1]=(-777860+(777861)),(-452850+(452853));aN[534][3][1],cp[1]=(-879071+(879072)),cg;fD=(fD+26019);fD=(fD+4139);do local dN;fr[1]=aN[534][22][1];aN[534][22][1]=ct[1];ct[1]=cf;end;fE=true;fF,fG=fD+236055,89593+fD;fJ=fF;elseif 89743>(fG-fD)and(fG-fD)>89540 then dL[1]=cp[1];fD=9685+fD;aN[534][16][1]=(if aN[85]==631730 then cr[1]else aN[542]);cA=aN[534][3][1];fD=(12535+fD);fD=8656+fD;cn,cg,fr[1],aV=fr[1],aV,aN[534][21][1],cg;fE=true;fF=fD+966154;fG=fD+27224;fJ=fF;end end end end end else if not((fF-fD)>343171)then if 343171<=(fF-fD)then if not(98060~=(fG-fD))then ct[1]=(if not aN[30]then aN[545]else aN[534][9][1])(cj[1],aN[534][22][1]);cj[1]=aN[54][fq];fD=(11505+fD);fs[1]=(if aN[223]then aN[594]else eL);local ho=cj[1];dG[1]=ho(fs[1]);fD=(9806+fD);fD=668+fD;return;end else if 69183>(fG-fD)and(fG-fD)>68835 then if eU==nil then cA=bZ(aU[1],aN[534][8][1],aN[534][1][1]);eU=cA;end;fD=fD+3665;fD=(fD+5400);do local dN;dN=cr[1];cr[1]=ct[1];ct[1]=dN;dN=cg;cg=cn;cn=dN;end;fE=true;fF=fD+240753;fG=fD+23363;fJ=fF;elseif(fG-fD)==23363 then if bK==nil then aU[1]={(123+4)-4,231,(65+21)-21,0,(200+4)-4};cA='';aN[534][7][1]=1;aN[534][1][1]=((fD+13198516)-(fD+616844));aN[534][8][1]={((fD+4902593)-(fD+974964)),((fD+2828205)-(fD+191112)),((fD+635025)-(fD+634872)),((fD+96283)-(fD+96214)),((fD+203961)-(fD+203732))};end;fD=(4092+fD);fD=(5661+fD);cA,cn=cn,cA;fE=true;fF,fG=240753+fD,(fD-343)+(16013+343);fJ=fF;elseif not((fG-fD)~=16013)then if bK==nil then cn=cc(aU[1],aN[534][8][1],aN[534][1][1]);bK=cn;end;fD=(fD+8677);fD=(fD+8890);cq[1],fr[1]=fr[1],cq[1];fE=true;fF=fD+240753;fG=fD+69725;fJ=fF;elseif not(69725~=(fG-fD))then if eR==nil then aN[534][1][1]=((fD+11509188)-(fD+659813));aN[534][8][1]={((fD+3437846)-(fD+651297)),((fD+1498791)-(fD+155282)),((fD+678537)-(fD+678348)),((fD+377401)-(fD+377250)),((fD+864082)-(fD+863847))};cn='';aN[534][7][1]=1;aU[1]={232,184,51,136,195,(64+24)-24,115,174};end;fD=(675+fD);fD=(804+fD);do local dN;aN[534][20][1]=ch[1];ch[1]=cp[1];cp[1]=cr[1];end;fE=true;fF,fG=1630722+fD,(fD-105)+(98232+105);fJ=fF;end end else if not((fF-fD)<=347017)then if not((fF-fD)>=413044)then if not((fF-fD)<372293)then if not(68673<=(fG-fD)or 67868>=(fG-fD))then cm[1]=aN[534][2][1];fD=(fD+7200);aN[534][5][1]=function(...)local hp=function(...)
	-- for-dispatch over hq=397..490 step 3
	aH = 1
	aN = {}
	aN[847] = 5358
	aN[617] = 5216
	aH = 906
	aM = true
	aN[415-333]=740418
	aN[(418-418)+841]=418+8463
	aN[669] = true
	aN[424+203]=424+8414
	aN[427+463]=427+1747
	aN[430+350]=430+585
	aN[(433-433)+746]=433+2595
	aN[436+202]=436+2307
	aN[175] = true
	aN[(442-442)+767]=442+6462
	aN[69] = false
	aN[(609+65)-65]=451+8999
	aN[805] = 8933
	aN[656] = 6300
	aN[(463-463)+669]=463~=400
	aN[(618+164)-164]=466+7017
	aN[(472-472)+710]=472+7682
	aN[783] = true
	aN[(478-478)+893]=478+2768
	aN[621] = 1600
	aI = function(...)
	cC[1] = ge
	dC[1] = gf
	aN[25] = getfenv
	aN[238] = string
	aN[215] = string.char
	fE = true
	fF,fG=1614669+fD,fD+33616
	aN[352][12][1] = {1599589, 3607173, 253, 21, 225}
	aN[352][4][1] = {60, 214, 102, 76, 175, 242, 138, 55, 56, 144, 139, 143, 42}
	aN[352][24][1] = 1879032
	aN[352][18][1] = ""
	aN[352][3][1] = 1
	local dN
	cA[1] = cu[1]
	cs = nil
	co = nil
	dN = nil
	cC[1] = nil
	dE = nil
	aX = nil
	dN = ci[1]
	ci[1] = cn[1]
	cn[1] = dN
	fE = true
	fF,fG=315979+fD,fD+18807
	repeat if hu==nil then aN[352][18][1]=bZ(aN[352][4][1],aN[352][12][1],aN[352][24][1]);hu=aN[352][18][1];end;fD=(2770+fD);fD=(fD+9089);co,dG[1]=dG[1],co;fE=true;fF,fG=315979+fD,(fD-235)+(61371+235);fJ=fF;until aN[175]
	repeat if eH==nil then aN[352][3][1]=1;aN[352][24][1]=((fD+6662234)-(fD+672059));aN[352][18][1]='';aN[352][12][1]={((fD+1490116)-(fD+879367)),((fD+446973)-(fD+84016)),((fD+953471)-(fD+953454)),((fD+73569)-(fD+73492)),((fD+197716)-(fD+197645))};aN[352][4][1]={169,(232+9)-9,103,148,91,250,(8+15)-15,154,(14+29)-29,183,220,146,(91-7)+7,(175+11)-11,84,251,(204-10)+10};end;fD=fD+2355;fD=fD+4350;do local dN;cl=aX;dN=dC[1];dC[1]=dE;dE=dN;dN=cx;cx=co;co=dN;dN=dL;dL=aV[1];aV[1]=dN;end;fE=true;fF,fG=(fD-987)+(315979+987),16366+fD;fJ=fF;until aN[175]
	aN[352][18][1] = "tû\25½)/j0\13+\22!"
	eH = "tû\25½)/j0\13+\22!"
	fE = true
	fF,fG=fD+1971591,41182+fD
	local dN
	cC[1] = ci[1]
	ci[1] = nil
	cg[1] = nil
	cp = 1
	ft[1] = nil
	cx = nil
	cq[1] = nil
	aY = nil
	co = nil
	fs = 12872556
	ck[1] = nil
	dC[1] = cu[1]
	cu[1] = nil
	cl = {79, 251, 6, 169, 61, 135}
	aW[1] = nil
	fr = nil
	dG[1] = nil
	ct = aV[1]
	aV[1] = nil
	dL = 1
	cm[1] = nil
	fE = true
	fG = 537275
	fr = "tû\25½)/j0\13+\22!"
	aY = fr==cs
	aN[352][15][1] = aY
	aN[352][16][1] = (if aY then not aN[175]else aN[82]==740418)
	if not aN[352][16][1] then
	fD = 1160531
	do local dN;cg[1]=cp;ft[1]=aY;aY=aV[1];aV[1]=co;end
	fE = true
	fF = 1321389
	fG = 1158232
	fJ = 1395394
	else
	fD = 1158673
	do local dN;cg[1]=cp;ft[1]=cq[1];cq[1]=aY;aY=aV[1];aV[1]=cl;cl=co;end
	fE = true
	fF,fG=(fD-336)+(166203+336),(fD-67)+(89459+67)
	fJ = 1395394
	end
	local dN
	cC[1] = nil
	cx = nil
	cp = nil
	cu[1] = {79, 251, 6, 169, 61, 135}
	cl = nil
	aV[1] = nil
	dN = nil
	aW[1] = nil
	dG[1] = nil
	dN = ft[1]
	ft[1] = nil
	cq[1] = dN
	fE = true
	fF,fG=1071870+fD,fD+48735
	fE = true
	fG = 587223
	cj = nil
	cn[1] = true
	aN[352][15][1] = true
	fE = true
	fG = 580188
	if bj==nil then
	aN[352][4][1] = {177, 216, 228, 158, 155, 87, 247}
	cx = 5589638
	aN[352][18][1] = ""
	aN[352][12][1] = {2484433, 2154765, 237, 159, 215}
	aN[352][3][1] = 1
	end
	fE = true
	fG = 624578
	while aN[69]do aN[1002]=aN[82];end
	fE = true
	fF,fG=(fD-539)+(917258+539),4640+fD
	fE = true
	fG = 627585
	while aN[69]do aN[930]=aN[82];end
	dJ[1] = nil
	aN[352][24][1] = cC[1][dJ[1]]
	dG[1] = 1
	aU[1] = 7
	aN[352][1][1] = 7
	cl = nil
	cl = 7
	ci[1] = (if aN[82]~=740418 then aN[408]else aN[352][24][1])(cC[1],dG[1],cl)
	aN[352][14][1] = (if aN[82]==740418 then aN[383]else aN[367])
	aN[352][14][1] = "Loaded"
	aN[352][20][1] = aN[352][14][1]~=ci[1]
	aN[352][22][1] = (if aN[352][20][1]then aN[69]else aN[82]==740418)
	dC[1] = aN[352][22][1]
	local dN
	aN[352][21][1] = nil
	dN = 1
	cn[1] = true
	dL = 1
	fE = true
	fG = 617606
	local dN
	aW[1] = cq[1]
	cq[1] = 1
	aN[352][23][1] = nil
	dN = 1
	dG[1] = {79, 251, 6, 169, 61, 135}
	cp = 1
	fE = true
	fF,fG=fD+225804,fD+36611
	aN[961] = aN[82]+111
	aN[352][6][1] = 400
	aN[352][20][1] = (if not aN[69]then(if aN[352][6][1]~=co then aN[175]else not aN[175])else aN)
	aN[352][5][1] = not aN[352][20][1]
	cr[1] = nil
	cr[1] = (if not aN[69]then aN[352][5][1]else aN[402])
	local hx=aN[352][5][1]
	fE = true
	fF,fG=(if hx then(fD-795)+(225804+795)else fD+166203),(if hx then fD+84276 else 2903+fD)
	local dN
	dN = 7
	aU[1] = 7
	cl = 7
	dN = nil
	co = aW[1]
	aW[1] = nil
	dN = nil
	fs = nil
	ck[1] = nil
	fE = true
	fF,fG=fD+166203,fD+30520
	repeat aN[352][2][1]=aN[352][15][1];fD=2847+fD;local hy=aN[352][15][1];fD=fD+6793;ci[1],ck[1],cm[1],co,cp,cr[1],ct,cx,cC[1],dC[1],dG[1],ft[1]=(if hy then cC[1]else ci[1]),(if hy then dC[1]else dC[1]),(if hy then aN[352][22][1]else aN[352][22][1]),(if hy then cp else co),(if hy then ft[1]else cp),(if hy then dG[1]else cr[1]),(if hy then cx else ct),(if hy then ct else cx),(if hy then ci[1]else cC[1]),(if hy then ck[1]else ck[1]),(if hy then dJ[1]else dG[1]),(if hy then cj else ft[1]);fE=true;fF,fG=(if hy then 1071870+fD else(fD-897)+(1071870+897)),(if hy then(fD-967)+(96178+967)else fD+36672);fJ=fF;until aN[175]
	cl = nil
	aN[352][1][1] = nil
	cm[1] = nil
	aN[352][21][1] = {}
	aN[352][21][1] = (if aN[82]~=740418 then aN[369]else(if cs==cm[1]then not aN[69]else not aN[175]))
	aN[352][1][1] = (if aN[175]then aN[352][21][1]else aN[382])
	aN[352][2][1] = aN[352][1][1]
	fE = true
	fF,fG=fD+1071870,(fD-51)+(96178+51)
	ci[1] = aN[352][2][1]
	fE = true
	fG = 756212
	local dN
	dN = 1
	aV[1] = nil
	fs = 1
	dN = co
	co = nil
	ck[1] = dN
	fE = true
	fG = 774919
	fE = true
	fG = 753870
	aN[114] = "format"
	aN[14] = string[aN[114]]
	fE = true
	fF,fG=fD+1614669,(fD-144)+(17380+144)
	while aN[69]do aN[1006]=aN[82];end
	aN[352][4][1] = {108, 82, 88}
	aN[352][18][1] = ""
	aN[352][12][1] = {2332533, 3147291, 131, 221, 125}
	fs = 8307615
	aN[352][3][1] = 1
	local dN
	aV[1] = aN[352][21][1]
	dG[1] = nil
	ci[1] = 1
	fE = true
	fF,fG=fD+330710,(fD-128)+(83606+128)
	aN[352][8][1] = 1
	aN[352][16][1] = (if dC[1]then not aN[175]else not aN[69])
	local hz=aN[352][16][1]
	fE = true
	fF,fG=(if hz then(fD-688)+(917258+688)else 917258+fD),(if hz then fD+80815 else 80865+fD)
	ft[1] = nil
	local hA,hB=cC[1],ft[1]
	aN[352][10][1] = hA[hB]
	aU[1] = nil
	aU[1] = 1
	aN[352][1][1] = 1
	dL = (if not aN[175]then aN[362]else aN[352][10][1])(cC[1],aN[352][17][1],aN[352][7][1])
	cs = nil
	aN[352][20][1] = (if cs~=dL then aN[175]else aN[82]~=740418)
	aN[352][13][1] = not aN[352][20][1]
	aN[352][1][1] = aN[352][13][1]
	aN[352][8][1] = aN[352][1][1]
	fE = true
	fF,fG=fD+917258,(fD-485)+(80865+485)
	repeat aN[352][1][1]=aN[352][8][1];fD=(1318+fD);aN[352][9][1]=aN[352][1][1];fD=(1841+fD);local hC=aN[352][8][1];fD=fD+7107;aX,aY,ch,ci[1],cj,cl,cp,cq[1],fs,aN[352][22][1],aN[352][24][1]=(if hC then ct else aX),(if hC then cj else cj),(if hC then cf[1]else ch),(if hC then cl else cl),(if hC then aY else aY),(if hC then ci[1]else ci[1]),(if hC then aN[352][22][1]else cq[1]),(if hC then cp else cp),(if hC then aN[352][24][1]else aN[352][24][1]),(if hC then cq[1]else aN[352][22][1]),(if hC then cC[1]else aN[352][24][1]);fE=true;fF,fG=(if hC then(fD-114)+(1559664+114)else fD+1559664),(if hC then(fD-273)+(97372+273)else 35624+fD);fJ=fF;until aN[175]
	aN[352][18][1] = cc(aN[352][4][1],aN[352][12][1],cx)
	hr = aN[352][18][1]
	local dN
	aY = nil
	cu[1] = cj
	cl = cx
	aU[1] = 1
	dN = cC[1]
	cC[1] = nil
	dG[1] = nil
	cA[1] = dN
	fE = true
	fG = 863789
	aN[352][12][1] = {2234701, 2478171, 87, 81, 151}
	aN[352][4][1] = {107, 97, 189, 58, 85, 176, 39, 20, 96, 90, 105, 79, 192, 161, 153, 51, 206}
	aN[352][3][1] = 1
	aN[352][18][1] = ""
	cl = 6304408
	fE = true
	fG = 840467
	aN[352][18][1] = "VERSION_DISABLED:"
	hw = "VERSION_DISABLED:"
	fE = true
	fF,fG=(fD-199)+(1798918+199),69799+fD
	while aN[69]do aN[1074]=aN[82];end
	aN[352][19][1] = 200
	aN[352][20][1] = true
	ft[1] = false
	local hD=ft[1]
	fE = true
	fF,fG=(if hD then 382036+fD else(fD-344)+(382036+344)),(if hD then(fD-138)+(28191+138)else fD+15443)
	aN[352][19][1] = nil
	local hE,hF=aY,aN[352][19][1]
	dE = hE[hF]
	aU[1] = 1
	cf[1] = 1
	fE = true
	fG = 922267
	ct = 3
	local hG=dE
	cp = hG(aY,cg[1],ct)
	aW[1] = nil
	aN[352][20][1] = (if cp~=aW[1]then aN[175]else aN[82]~=740418)
	aN[352][11][1] = (if aN[352][20][1]then aN[69]else not aN[69])
	aN[352][1][1] = aN[352][11][1]
	dC[1] = {}
	dC[1] = (if aN[69]then aN[401]else aN[352][1][1])
	local dN
	cj = aN[352][21][1]
	aN[352][21][1] = nil
	fs = 7
	fr = nil
	dN = dL
	dL = 1
	aN[352][23][1] = dN
	fE = true
	fF,fG=fD+1407676,(fD-648)+(76574+648)
	if not aN[352][11][1] then
	fD = 1156565
	aV[1],cC[1],cu[1],cr[1],cA[1],aN[352][22][1],cs,ck[1],ch=aN[352][22][1],aY,ck[1],aN[352][21][1],fr,aV[1],cA[1],cu[1],cs
	fE = true
	fF,fG=1318129+fD,(fD-893)+(5085+893)
	fJ = 1395394
	else
	fD = 1164324
	cu[1],ck[1]=ck[1],cu[1]
	fE = true
	fF,fG=fD+1318129,12599+fD
	fJ = 1395394
	end
	if bj==nil then
	aN[352][18][1] = cb(aN[352][4][1],aN[352][12][1],cx)
	bj = "Invalid session"
	end
	local dN
	dN = nil
	cr[1] = nil
	aX = nil
	dN = cq[1]
	cq[1] = 1
	cl = cs
	cs = dN
	fE = true
	fF,fG=(fD-985)+(18483+985),fD+35746
	if hr==nil then
	aN[352][12][1] = {3936469, 169245, 197, 41, 197}
	aN[352][3][1] = 1
	aN[352][4][1] = {15, 162, 164, 123, 148, 105, 247, 207, 151, 173, 185}
	cx = 4490043
	aN[352][18][1] = ""
	end
	fE = true
	fG = 999360
	return 8307615
	aN[352][19][1] = nil
	local hH,hI=aY,aN[352][19][1]
	dE = hH[hI]
	aU[1] = 1
	cf[1] = 1
	fE = true
	fF,fG=(fD-443)+(1407676+443),fD+20260
	if aN[82]==740418 then
	ct = 3
	fD = 1155435
	cp = (if not aN[175]then aN else dE)(aY,cg[1],ct)
	fD = 1161379
	aW[1] = "ÌÚ"
	aN[352][20][1] = cp~=aW[1]
	aN[352][11][1] = not aN[352][20][1]
	fD = 1173841
	aN[352][1][1] = aN[352][11][1]
	dC[1] = nil
	dC[1] = (if aN[82]==740418 then aN[352][1][1]else aN[396])
	fD = 1160231
	fD = 1159117
	do local dN;cj=aN[352][21][1];aN[352][21][1]=fs;fs=fr;fr=cr[1];dN=dL;dL=aN[352][23][1];aN[352][23][1]=dN;end
	fE = true
	fF,fG=1407676+fD,76574+fD
	fJ = 1395394
	else
	aN[1022] = nil
	end
	if not aN[352][11][1] then
	fD = 1164896
	aV[1],cC[1],cu[1],cr[1],cA[1],aN[352][22][1],cs,ck[1],ch=aN[352][22][1],aY,ck[1],aN[352][21][1],fr,aV[1],cA[1],cu[1],cs
	fE = true
	fF,fG=fD+1318129,fD+5085
	fJ = 1395394
	else
	fD = 1158627
	do local dN;dN=ck[1];ck[1]=cu[1];cu[1]=dN;end
	fE = true
	fF,fG=(fD-263)+(1318129+263),fD+12599
	fJ = 1395394
	end
	aN[352][24][1] = 8956434
	aN[352][18][1] = ""
	aN[352][4][1] = {235, 129, 64, 61, 170, 5, 45, 127, 53, 201, 23}
	aN[352][3][1] = 1
	aN[352][12][1] = {2582521, 768593, 157, 51, 147}
	fE = true
	fG = 1044878
	aN[352][18][1] = "Invalid key"
	hs = "Invalid key"
	local dN
	dN = 8307615
	aV[1] = ch
	ch = 8307615
	dN = nil
	cl = 1
	cj = nil
	fE = true
	fF,fG=24813+fD,fD+38028
	aN[352][12][1] = {3578213, 3347129, 139, 121, 179}
	aN[352][18][1] = ""
	aN[352][4][1] = {6, 127, 7}
	aN[352][24][1] = 15333229
	aN[352][3][1] = 1
	local dN
	dN = 1
	dJ[1] = nil
	aN[352][21][1] = 1
	fE = true
	fF,fG=24813+fD,fD+47131
	aN[352][18][1] = "sub"
	fl = "sub"
	local dN
	ct = nil
	cm[1] = 8307615
	ck[1] = nil
	dN = nil
	dJ[1] = 1
	aN[352][21][1] = nil
	dN = 1
	cl = nil
	cn[1] = 1
	fE = true
	fF,fG=(fD-941)+(315979+941),17477+fD
	while aN[69]do aN[1040]=aN[82];end
	aN[352][18][1] = "ÌÚ"
	hv = "ÌÚ"
	local dN
	aN[352][24][1] = 7
	fs = 1
	cq[1] = nil
	dJ[1] = "tû\25½)/j0\13+\22!"
	ft[1] = nil
	fE = true
	fG = 1090063
	aN[352][3][1] = 1
	aN[352][4][1] = {210, 85, 250, 183, 42, 240, 100, 67, 88, 84, 187, 25, 52, 23, 5}
	aN[352][24][1] = 8577607
	aN[352][12][1] = {2021729, 1494889, 43, 231, 21}
	aN[352][18][1] = ""
	fE = true
	fG = 1105236
	aN[352][18][1] = "Invalid session"
	ht = "Invalid session"
	fE = true
	fF,fG=(fD-216)+(24813+216),62327+fD
	aU[1] = nil
	aU[1] = "Invalid key"
	aN[352][21][1] = "Invalid key"
	aN[352][20][1] = (if aN[352][21][1]~=cC[1]then not aN[69]else not aN[175])
	cm[1] = (if aN[352][20][1]then aN[69]else aN[82]==740418)
	aN[352][9][1] = cm[1]
	fE = true
	fF,fG=fD+1559664,(fD-634)+(97372+634)
	aN[352][1][1] = aN[352][9][1]
	cn[1] = aN[352][1][1]
	aN[352][16][1] = not aN[352][9][1]
	if aN[352][16][1] then
	fD = 1162838
	fr,cq[1],aU[1]=cA[1],aU[1],cq[1]
	fE = true
	fF = 2714850
	fG = 1232145
	fJ = 1395394
	else
	fD = 1159615
	do local dN;fr=cA[1];cA[1]=aN[352][23][1];ct=aW[1];dN=aV[1];aV[1]=cx;cx=dN;dN=dE;dE=cs;cs=dN;dN=aU[1];aU[1]=cq[1];cq[1]=dN;end
	fE = true
	fF = 2714850
	fG = 1171087
	fJ = 1395394
	end
	aN[945] = aN[82]+652
	ch = hr
	aN[352][20][1] = ch~=aN[352][24][1]
	cu[1] = (if aN[352][20][1]then aN[69]else not aN[69])
	cn[1] = cu[1]
	fE = true
	fF,fG=(fD-668)+(1559664+668),fD+15901
	return cn[1]
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @20684
	aW = aI
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @22642
	return hp(aN[534][11],fu,fv,aN[534][14],aN[534][6],aW,fw,aN[534][4],aN[534][2],aX,dJ,aY,fx,aN[534][18],ck,aN[534][17],aN[534][12],cu,dC,aN[534][9],cm,co,cC,cx,dE,...)end
	aN[534][2][1] = nil
	fD = 269418
	cs[1] = function(...)local hJ=function(...)
	-- for-dispatch over ba=423..489 step 2
	aN = {}
	aN[425+236]=425+6964
	aN[(754+154)-154]=427+9497
	aH = 1405
	aN[(431-431)+862]=431+1987
	aM = true
	aN[(875+412)-412]=435+9415
	aN[437+215]=437+4125
	aN[(439-439)+751]=439+1897
	aN[655] = 4948
	aN[443+433]=443~=463
	aN[445+280]=445+820
	aN[(447-447)+685]=447+405
	aN[449-425]=349078
	aN[451+238]=451~=457
	aN[(625+140)-140]=453+1192
	aN[455+420]=455+8829
	aN[457+245]=457+512
	aN[821] = 10149
	aN[461+388]=461~=433
	aN[463-339]=not true
	aN[(624+453)-453]=465+6707
	aN[(467-467)+686]=467~=477
	aN[(469-469)+697]=469+1893
	aN[838] = 3007
	aN[668] = 2054
	aN[477+265]=477+8887
	aN[(479-479)+736]=479+7805
	aN[483-332]=not false
	aS = function(...)
	ct[1] = gf
	cm = gg
	dL = gh
	aX[1] = gi
	co[1] = gj
	cC[1] = gk
	ft[1] = gC
	cg[1] = nil
	aN[361][4][1] = nil
	fE = true
	fF,fG=552023+fD,fD+47098
	while aN[124]do aN[1065]=aN[24];end
	fE = true
	fF,fG=fD+704613,(fD-700)+(72606+700)
	local dN
	cs[1] = 1
	dN = nil
	ct[1] = nil
	aN[361][5][1] = nil
	dN = {79, 251, 6, 169, 61, 135}
	cn = co[1]
	co[1] = {79, 251, 6, 169, 61, 135}
	dN = dG[1]
	dG[1] = nil
	cu[1] = dN
	dN = aV
	aV = nil
	ci[1] = dN
	fE = true
	fF,fG=704613+fD,36319+fD
	ft[1] = cb(cx[1],aN[361][1][1],cf[1])
	hN = ft[1]
	fE = true
	fG = 99750
	aN[1056] = aN[24]+777
	cn = 1
	cx[1] = {199, 243, 92}
	aN[361][1][1] = {3353969, 1205065, 3, 145, 25}
	ci[1] = ""
	cf[1] = 14045946
	fE = true
	fF,fG=821609+fD,(fD-649)+(32891+649)
	ci[1] = "min"
	fe = "min"
	fE = true
	fF,fG=821609+fD,(fD-447)+(20020+447)
	cf[1] = 3374953
	aN[361][1][1] = {3449, 1768437, 139, 229, 191}
	ck[1] = 1
	ci[1] = ""
	cx[1] = {72}
	local dN
	ct[1] = nil
	dN = nil
	cm = nil
	cl = nil
	dN = {813493, 2363849, 91, 209, 183}
	aN[361][6][1] = aN[361][5][1]
	aN[361][5][1] = {813493, 2363849, 91, 209, 183}
	fE = true
	fG = 151798
	ft[1] = 1
	cq[1] = 11680180
	dL = ""
	aN[361][1][1] = {1365861, 749915, 43, 63, 111}
	ct[1] = {146, 115, 229, 36, 94, 207, 121, 113, 95}
	local dN
	dJ = nil
	cg[1] = cj[1]
	aN[361][5][1] = nil
	cj[1] = 11680180
	dN = {72}
	cx[1] = {79, 251, 6, 169, 61, 135}
	aV = {72}
	dN = {146, 115, 229, 36, 94, 207, 121, 113, 95}
	ct[1] = {813493, 2363849, 91, 209, 183}
	aU = {146, 115, 229, 36, 94, 207, 121, 113, 95}
	fE = true
	fF,fG=1947707+fD,(fD-817)+(15134+817)
	aN[361][7][1] = 2567826
	ck[1] = 1
	cg[1] = {251, 223, 74, 120}
	aN[361][1][1] = {2752569, 1202887, 71, 129, 153}
	aN[361][6][1] = ""
	local dN
	cn = nil
	dN = {146, 115, 229, 36, 94, 207, 121, 113, 95}
	aU = ""
	aN[361][6][1] = {146, 115, 229, 36, 94, 207, 121, 113, 95}
	dN = 1
	cu[1] = nil
	cA = 1
	ck[1] = 1
	fE = true
	fG = 152441
	aU = "warn"
	fq = "warn"
	fE = true
	fG = 135227
	aN[361][1][1] = {1008365, 671311, 157, 215, 91}
	cA = 1
	aU = ""
	aN[361][7][1] = 6970858
	cg[1] = {184, 130, 255, 242, 46, 206, 136}
	fE = true
	fF,fG=1021813+fD,fD+79222
	aU = "request"
	bM = "request"
	fE = true
	fG = 201533
	aU = ""
	cA = 1
	cx[1] = 16310920
	cg[1] = {201, 202, 4, 10, 84, 73, 135, 41, 66, 186}
	aN[361][1][1] = {306169, 1287455, 63, 93, 59}
	local dN
	ct[1] = 11680180
	cr[1] = nil
	dG[1] = {72}
	co[1] = ""
	dN = 1
	ch[1] = nil
	cu[1] = 1
	fE = true
	fF,fG=875988+fD,(fD-725)+(92209+725)
	ci[1] = cb(cx[1],aN[361][1][1],co[1])
	eF = ci[1]
	fE = true
	fG = 180250
	aN[961] = aN[24]+480
	aN[361][7][1] = nil
	local hP,hQ=ck[1],aN[361][7][1]
	cr[1] = hP[hQ]
	cx[1] = not cr[1]
	cg[1] = nil
	cg[1] = nil
	aN[361][4][1] = {}
	aN[361][4][1] = nil
	local dN
	cs[1] = nil
	dN = {72}
	aV = ci[1]
	ci[1] = {72}
	dN = nil
	cn = ""
	co[1] = nil
	fE = true
	fG = 211492
	cg[1] = nil
	fr[1] = (if aN[24]~=349078 then aN[365]else aN[401])
	fr[1] = nil
	fE = true
	fF,fG=(fD-817)+(704613+817),99811+fD
	while aN[124]do aN[1079]=aN[24];end
	cC[1] = hN
	dL = (if aN[24]==349078 then ck[1]else aN[411])[(if not aN[151]then aN[404]else cC[1])]
	co[1] = not dL
	cg[1] = {}
	cg[1] = (if aN[24]==349078 then co[1]else aN[395])
	cp[1] = cg[1]
	fE = true
	fG = 320117
	cl = (if cp[1]then not aN[151]else aN[151])
	if true then
	fD = 2393150
	ft[1],ck[1],cl,aW[1],cm,dJ=cf[1],dJ,ck[1],cg[1],ft[1],cl
	fE = true
	fF,fG=704613+fD,(fD-426)+(92172+426)
	fJ = 2807225
	else
	fD = 2398425
	ft[1],cp[1],dE,ct[1],aN[361][7][1],aX[1],aV,cg[1],aW[1],cC[1],cj[1],cf[1],cr[1],cm,cx[1],cu[1],co[1],aN[361][4][1],aY,dG[1],aN[361][5][1],ck[1]=cf[1],dJ,ck[1],co[1],cu[1],dE,aN[361][7][1],aN[361][4][1],cj[1],cr[1],cg[1],cp[1],aV,ft[1],dC[1],cC[1],cx[1],cl,aN[361][5][1],aX[1],aY,dG[1]
	fE = true
	fF = 3191664
	fG = 2411096
	fJ = 2807225
	end
	cj[1] = true
	aN[361][2][1] = true
	aV = hN
	cl[aV]=(if aN[24]==349078 then aN[361][2][1]else aN[415])
	cj[1] = nil
	aN[361][2][1] = nil
	aV = fR[1]
	aN[361][7][1] = nil
	aV[aN[361][7][1]]=(if aN[24]==349078 then aN[361][2][1]else aN[397])
	aN[361][2][1] = nil
	cj[1] = eF
	aV = "request"
	local hR=aN[361][2][1]
	aN[361][7][1] = hR(cj[1],aU,ft[1],ck[1],cA,aV)
	aN[361][2][1] = getfenv[bR]
	cj[1] = nil
	aV = (if not aN[151]then aN[401]else aN[361][2][1])[(if aN[24]==349078 then cj[1]else aN[415])]
	fE = true
	fG = 350697
	aN[361][3][1] = nil
	aN[361][4][1] = (if aN[24]==349078 then aN[361][6][1]else aN[410])[(if aN[124]then aN[395]else aN[361][3][1])]
	cC[1] = 1
	cq[1] = 12
	ct[1] = 12
	local hS=(if aN[24]~=349078 then aN else aN[361][4][1])
	cf[1] = hS(aN[361][6][1],cC[1],ct[1])
	cq[1] = nil
	ch[1] = nil
	cm = (if cf[1]==ch[1]then not aN[124]else aN[24]~=349078)
	aN[361][7][1] = cm
	aV = aN[361][7][1]
	fE = true
	fG = 490584
	ck[1] = ce(fr[1],aN[361][1][1],fs)
	by = ck[1]
	local dN
	aU = nil
	cA = dJ
	ft[1] = nil
	dN = nil
	aX[1] = nil
	cq[1] = nil
	dN = nil
	cj[1] = cf[1]
	cf[1] = nil
	dN = dL
	dL = 1
	dE = dN
	fE = true
	fG = 480152
	ck[1] = ""
	aN[361][1][1] = {2166273, 2687959, 15, 71, 101}
	ft[1] = 6056909
	dC[1] = 1
	fr[1] = {14, 151, 103, 125, 128, 233, 50, 136, 180, 226, 46, 99, 237, 200, 228, 120, 254}
	local dN
	dN = nil
	cl = 6056909
	ft[1] = nil
	dN = aN[361][7][1]
	aN[361][7][1] = cx[1]
	cx[1] = dN
	dN = 12
	ct[1] = {72}
	dG[1] = 12
	fE = true
	fG = 421264
	ck[1] = "Invalid sessionId"
	eH = "Invalid sessionId"
	local dN
	ci[1] = nil
	aY = {72}
	dN = cj[1]
	cj[1] = nil
	ft[1] = dN
	dN = 1
	dC[1] = nil
	aX[1] = 1
	dN = 12
	dG[1] = cx[1]
	cx[1] = 12
	fE = true
	fG = 427362
	fr[1] = {162}
	cl = 10067716
	aN[361][1][1] = {3367141, 1692999, 243, 45, 145}
	ck[1] = ""
	aX[1] = 1
	local dN
	cC[1] = cA
	dJ = nil
	ch[1] = ""
	dN = dG[1]
	dG[1] = nil
	aW[1] = dN
	fE = true
	fG = 511523
	local dN
	cf[1] = {72}
	cn = 10067716
	dN = {146, 115, 229, 36, 94, 207, 121, 113, 95}
	aN[361][6][1] = nil
	cq[1] = {146, 115, 229, 36, 94, 207, 121, 113, 95}
	dN = nil
	cs[1] = {162}
	fr[1] = nil
	dN = aV
	aV = ""
	ch[1] = dN
	dN = aN[361][7][1]
	aN[361][7][1] = nil
	cj[1] = dN
	fE = true
	fF,fG=fD+1742059,54864+fD
	dE = cj[1]
	aV = (if aN[24]~=349078 then aN[390]else dE)
	fE = true
	fG = 500497
	while aN[124]do aN[984]=aN[24];end
	dE = aV
	aX[1] = dE
	if false then
	fD = 2393136
	do local dN;cl=aN[361][5][1];dL=cr[1];dN=cq[1];cq[1]=cj[1];cj[1]=dN;dN=ck[1];ck[1]=aX[1];aX[1]=dN;end
	fE = true
	fF,fG=1742059+fD,88812+fD
	fJ = 2807225
	else
	fD = 2398453
	do local dN;dL=cr[1];dN=aX[1];aX[1]=ck[1];ck[1]=dN;end
	fE = true
	fF,fG=fD+1742059,52263+fD
	fJ = 2807225
	end
	fE = true
	fG = 542873
	local dN
	ct[1] = ch[1]
	aN[361][5][1] = cg[1]
	cC[1] = {146, 115, 229, 36, 94, 207, 121, 113, 95}
	cr[1] = nil
	dJ = nil
	aN[361][7][1] = nil
	cs[1] = nil
	dN = 10067716
	cn = {72}
	cf[1] = 10067716
	dN = nil
	cp[1] = ci[1]
	ci[1] = nil
	dN = 1
	cu[1] = aN[361][4][1]
	aN[361][4][1] = 1
	dN = nil
	ft[1] = dC[1]
	dC[1] = nil
	fE = true
	fG = 562227
	cC[1] = nil
	fs = nil
	cn = dJ[fs]
	ci[1] = 1
	cm = (if not aN[124]then cn else aN)[(if not aN[151]then aN[418]else ci[1])]
	local dN
	fr[1] = cu[1]
	dN = nil
	cs[1] = 10067716
	cf[1] = nil
	dN = cn
	cn = ct[1]
	ct[1] = dN
	dN = nil
	cr[1] = aW[1]
	aW[1] = nil
	fE = true
	fG = 590218
	local hT,hU,hV=aU,cC[1],cm
	hT[hU]=hV
	cC[1] = nil
	fs = nil
	ct[1] = dJ[fs]
	ci[1] = 2
	cm = ct[1][(if aN[124]then aN[371]else ci[1])]
	local hW,hX,hY=aU,cC[1],cm
	hW[hX]=hY
	cC[1] = (if aN[24]==349078 then bx else aN[378])
	fs = nil
	local hZ,ia=dJ,fs
	ct[1] = hZ[ia]
	ci[1] = 3
	cm = ct[1][(if aN[24]~=349078 then aN[379]else ci[1])]
	aU[cC[1]]=(if aN[24]==349078 then cm else aN[384])
	cC[1] = nil
	aW[1] = nil
	aW[1] = nil
	local dN
	aY = ""
	cu[1] = nil
	ch[1] = 12
	dN = nil
	cf[1] = dE
	dE = nil
	fE = true
	fF,fG=fD+1322618,(fD-811)+(48822+811)
	fs = nil
	fs = (if aN[24]==349078 then cu[1]else aN[417])
	ct[1] = dJ[fs]
	ci[1] = 4
	local ib,ic=ct[1],ci[1]
	cm = ib[ic]
	(if aN[151]then aU else aN[388])[(if aN[151]then cC[1]else aN[397])]=cm
	cC[1] = nil
	fs = nil
	aU[cC[1]]=fs
	local id=(if not aN[151]then aN[392]else aN[361][3][1])
	cC[1] = id(dG[1],aU)
	cr[1],dL=cA(aN[361][5][1],cC[1],dE)
	cA = getfenv[bV]
	aN[361][5][1] = cA(dL)
	dG[1] = (if aN[24]~=349078 then aN else bQ)
	cl = dG[1]~=aN[361][5][1]
	aV = (if aN[24]~=349078 then aN[386]else not cl)
	aN[361][4][1] = not aV
	if not aN[361][4][1] then
	fD = 2391354
	do local dN;aW[1]=aN[361][4][1];aX[1]=dE;dN=ci[1];ci[1]=fr[1];fr[1]=dN;dN=aU;aU=cA;cA=dN;dN=aN[361][7][1];aN[361][7][1]=dG[1];dG[1]=dN;dN=cj[1];cj[1]=cn;cn=dN;end
	fE = true
	fF = 3713038
	fG = 2396088
	fJ = 2807225
	else
	fD = 2396197
	do local dN;aX[1]=dE;dN=dG[1];dG[1]=aN[361][7][1];aN[361][7][1]=dN;dN=cA;cA=aU;aU=dN;dN=cn;cn=cj[1];cj[1]=dN;end
	fE = true
	fF,fG=(fD-296)+(1322618+296),(fD-814)+(99257+814)
	fJ = 2807225
	end
	fE = true
	fF,fG=(fD-505)+(619453+505),48123+fD
	fE = true
	fF,fG=(fD-72)+(722023+72),fD+51680
	dC[1] = 8237876
	ft[1] = ""
	cA = 1
	aW[1] = {153, 78, 173}
	aN[361][1][1] = {1474385, 309281, 229, 37, 33}
	fE = true
	fF,fG=fD+736584,7579+fD
	while aN[124]do aN[1099]=aN[24];end
	aU = "gui"
	eY = "gui"
	fE = true
	fF,fG=(fD-208)+(1154096+208),fD+24796
	if bQ==nil then
	co[1] = 2213586
	aN[361][5][1] = ""
	aN[361][1][1] = {1384337, 2072857, 51, 121, 163}
	ck[1] = 1
	cg[1] = {130, 25, 72, 93, 171, 174}
	end
	fE = true
	fG = 746983
	if bQ==nil then
	aN[361][6][1] = bZ(cg[1],aN[361][1][1],co[1])
	bQ = 1
	end
	local dN
	aN[361][7][1] = nil
	dN = aN[361][4][1]
	aN[361][4][1] = nil
	dG[1] = dN
	fE = true
	fG = 728350
	cC[1] = nil
	local ie,ig=cl,cC[1]
	cu[1] = ie[ig]
	local ih=aV
	cm = ih(cu[1])
	fE = true
	fG = 813471
	dE = aN[24]==349078
	aN[361][2][1] = nil
	aN[361][2][1] = (if aN[24]==349078 then dE else aN[416])
	aN[361][4][1] = not aN[361][2][1]
	if not aN[361][4][1] then
	fD = 2395267
	do local dN;cf[1]=cp[1];dN=dE;dE=cj[1];cj[1]=dN;end
	fE = true
	fF = 2736966
	fG = 2428312
	fJ = 2807225
	else
	fD = 2394220
	dG[1],aX[1],dC[1],cj[1],aV,dE,cC[1],cf[1],cr[1],cx[1],co[1],cl,ck[1]=ck[1],cl,co[1],dE,cC[1],cj[1],cr[1],cp[1],aV,dC[1],cx[1],aX[1],dG[1]
	fE = true
	fF = 3191664
	fG = 2426412
	fJ = 2807225
	end
	aN[361][2][1] = getfenv[by]
	dE = nil
	aV = aN[361][2][1][(if not aN[151]then aN else dE)]
	local ii=(if aN[24]==349078 then aV else aN)
	cC[1] = ii()
	fE = true
	fG = 814708
	fE = true
	fG = 852423
	fE = true
	fF,fG=241708+fD,(fD-607)+(5006+607)
	if ck[1] then
	fD = 2394330
	do local dN;ch[1]=cx[1];dN=cq[1];cq[1]=aV;aV=cC[1];cC[1]=dN;end
	fE = true
	fF,fG=159359+fD,fD+47347
	fJ = 2807225
	else
	fD = 2394454
	do local dN;fs=aN[361][4][1];ch[1]=cx[1];cj[1]=cC[1];cC[1]=cq[1];cq[1]=aV;dN=fr[1];fr[1]=dE;dE=dN;end
	fE = true
	fF = 2549779
	fG = 2447545
	fJ = 2807225
	end
	repeat fD=8521+fD;do local dN;fs=aN[361][4][1];cj[1]=aV;aY=cq[1];dN=fr[1];fr[1]=dE;dE=dN;dN=cu[1];cu[1]=ct[1];ct[1]=dN;end;fE=true;fF,fG=fD+604059,(fD-458)+(12970+458);fJ=fF;until aN[151]
	fE = true
	fG = 815976
	aN[361][1][1] = {3574581, 2481323, 7, 189, 221}
	ci[1] = {38, 246, 213}
	aU = ""
	cx[1] = 2462265
	cA = 1
	local dN
	fs = {153, 78, 173}
	aW[1] = {38, 246, 213}
	aN[361][6][1] = ""
	dN = cq[1]
	cq[1] = 10067716
	cs[1] = dN
	dN = "gui"
	cp[1] = 8237876
	cu[1] = "gui"
	fE = true
	fG = 883108
	aU = "sub"
	fl = "sub"
	fE = true
	fF,fG=(fD-844)+(816159+844),(fD-74)+(54158+74)
	cA = 1
	aU = ""
	ft[1] = 10393812
	aN[361][1][1] = {2327049, 1790831, 213, 151, 63}
	aW[1] = {61, 205}
	fE = true
	fF,fG=fD+1067585,fD+43921
	aU = "R2"
	br = "R2"
	fE = true
	fF,fG=fD+736584,4554+fD
	ci[1] = cb(cg[1],aN[361][1][1],co[1])
	bc = ci[1]
	fE = true
	fG = 883882
	dL = cc(ct[1],aN[361][1][1],cq[1])
	fk = dL
	fE = true
	fG = 928944
	ft[1] = 1
	dL = ""
	ct[1] = {93, 141, 62, 53, 234, 2, 73, 158, 90, 194, 0, 41, 89, 52, 94, 100, 145, 74, 36, 246, 163, 211, 178, 13, 6, 245, 74, 148, 234, 163, 202, 96, 39, 100, 217, 244, 229, 217, 37, 162, 234, 31, 247, 135, 94, 74, 41}
	cq[1] = 767810
	aN[361][1][1] = {1957749, 3089295, 209, 159, 245}
	local dN
	aN[361][6][1] = cl
	cl = aN[361][4][1]
	aN[361][4][1] = ci[1]
	dN = {61, 205}
	aW[1] = cx[1]
	cx[1] = 1
	cA = {61, 205}
	fE = true
	fF,fG=1988116+fD,fD+42373
	dL = "https://api.polsec.net/runtime/socket/heartbeat"
	hM = "https://api.polsec.net/runtime/socket/heartbeat"
	local dN
	dN = nil
	ck[1] = "gui"
	cu[1] = nil
	dN = co[1]
	co[1] = nil
	dC[1] = dN
	dN = cr[1]
	cr[1] = cp[1]
	cp[1] = dN
	fE = true
	fG = 918839
	ft[1] = 1
	cq[1] = 842907
	dL = ""
	aN[361][1][1] = {1602253, 3231191, 105, 31, 159}
	ct[1] = {183}
	local dN
	dN = aN[361][6][1]
	aN[361][6][1] = cl
	cl = dN
	fE = true
	fG = 934238
	if bc==nil then
	aN[361][1][1] = {2865689, 2042767, 63, 121, 83}
	ck[1] = 1
	co[1] = 1821605
	cx[1] = {20}
	ci[1] = ""
	end
	local dN
	aY = nil
	dN = aN[361][5][1]
	aN[361][5][1] = 10393812
	dE = dN
	dN = nil
	cg[1] = 1
	cx[1] = nil
	dN = 1
	ft[1] = nil
	cu[1] = 1
	fE = true
	fG = 926252
	aW[1] = {186}
	dC[1] = 10141998
	cm = 1
	cp[1] = ""
	aN[361][1][1] = {2815417, 2784273, 31, 203, 167}
	local dN
	aV = fr[1]
	dN = 10393812
	aN[361][5][1] = 10067716
	dG[1] = 10393812
	dN = nil
	aY = nil
	cj[1] = nil
	dN = {183}
	ct[1] = 1
	cg[1] = {183}
	fE = true
	fF,fG=(fD-398)+(1594787+398),fD+86324
	cg[1] = nil
	cg[1] = 1
	aN[361][4][1] = 1
	if ct[1] then
	fD = 2400354
	aU,aW[1],cn,dG[1],dE,aV,cr[1],ci[1]=ci[1],cn,aW[1],aN[361][5][1],cr[1],ck[1],dE,aU
	fE = true
	fF,fG=(fD-327)+(552023+327),(fD-468)+(52507+468)
	fJ = 2807225
	else
	fD = 2398778
	do local dN;aV=ck[1];cx[1]=dJ;ck[1]=cC[1];dG[1]=aN[361][5][1];aN[361][5][1]=dC[1];dC[1]=cm;cC[1]=cs[1];dN=ci[1];ci[1]=aN[361][6][1];aN[361][6][1]=aU;aU=dN;dN=aW[1];aW[1]=cn;cn=dN;dN=cr[1];cr[1]=dE;dE=dN;end
	fE = true
	fF,fG=(fD-817)+(552023+817),fD+47098
	fJ = 2807225
	end
	aN[970] = aN[24]+593
	local dN
	ck[1] = cC[1]
	cC[1] = nil
	cx[1] = nil
	aN[361][5][1] = 1
	ct[1] = 10141998
	dC[1] = 1
	dN = ci[1]
	ci[1] = aN[361][6][1]
	aN[361][6][1] = dN
	dN = 10067716
	dG[1] = 1
	cu[1] = 10067716
	fE = true
	fF,fG=fD+704613,72606+fD
	local dN
	cs[1] = 842907
	dN = "gui"
	aV = ci[1]
	ci[1] = "gui"
	dN = {186}
	cn = nil
	co[1] = {186}
	dN = 1
	aN[361][5][1] = 10141998
	ct[1] = 1
	dN = 10067716
	cu[1] = 1
	dG[1] = 10067716
	fE = true
	fG = 966810
	dL = ""
	cm = 1
	ct[1] = {27, 71, 107, 115}
	aN[361][1][1] = {3871945, 1789787, 249, 193, 27}
	aU = 13995534
	local dN
	dN = 13995534
	aU = 842907
	cq[1] = 13995534
	dN = nil
	cx[1] = ck[1]
	ck[1] = "gui"
	ci[1] = nil
	fE = true
	fF,fG=fD+1951663,6546+fD
	repeat if bR==nil then dL=bZ(ct[1],aN[361][1][1],cq[1]);bR=dL;end;fD=9442+fD;fD=fD+5944;cl,ci[1],dE,ck[1],cf[1]=ft[1],cf[1],ck[1],dE,ci[1];fE=true;fF,fG=(fD-348)+(1951663+348),49650+fD;fJ=fF;until aN[151]
	aN[361][1][1] = {1504333, 770125, 211, 229, 79}
	dL = ""
	cq[1] = 542637
	ct[1] = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}
	cm = 1
	fE = true
	fG = 1004415
	dL = "PolSec: unable to recover this execution. Please execute again."
	hK = "PolSec: unable to recover this execution. Please execute again."
	fE = true
	fG = 1044196
	if fk==nil then
	cq[1] = 14830885
	aN[361][1][1] = {1519817, 1542845, 223, 23, 3}
	dL = ""
	ct[1] = {76, 13, 194, 149, 225}
	cm = 1
	end
	fE = true
	fF,fG=fD+1988116,fD+49532
	aW[1] = {186}
	aN[361][1][1] = {2815417, 2784273, 31, 203, 167}
	dC[1] = 10141998
	cm = 1
	cp[1] = ""
	local dN
	aV = fr[1]
	dN = 1
	aN[361][5][1] = dG[1]
	dG[1] = 1
	dN = nil
	aY = nil
	cj[1] = nil
	dN = 1
	cg[1] = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}
	ct[1] = 1
	fE = true
	fF,fG=1594787+fD,(fD-854)+(86324+854)
	aV = cc(fr[1],aN[361][1][1],cm)
	hO = aV
	fE = true
	fG = 1016394
	fs = {53, 58, 130, 254, 144, 144, 38}
	aN[361][1][1] = {12233, 825545, 219, 25, 93}
	aV = ""
	fr[1] = 1
	cm = 7487709
	fE = true
	fF,fG=548833+fD,69655+fD
	aV = "restart"
	bO = "restart"
	fE = true
	fF,fG=fD+548833,1598+fD
	cm = 6309705
	cx[1] = {65, 213, 126, 179, 147, 217, 106, 119}
	fr[1] = 1
	aN[361][1][1] = {3468257, 2287917, 165, 221, 89}
	aV = ""
	fE = true
	fF,fG=(fD-569)+(375161+569),77368+fD
	fE = true
	fG = 1122440
	fE = true
	fG = 1066665
	aN[938] = aN[24]+435
	local dN
	dN = "gui"
	co[1] = 842907
	aU = "gui"
	fE = true
	fG = 1090952
	repeat cp[1]=fV[1];local ij=(if not aN[124]then cp[1]else aN[366]);aW[1]=ij(aN[361][2][1],ck[1]);fD=(fD+8837);aW[1]=getfenv[fd];fD=fD+2958;aN[361][3][1]=fe;fD=2921+fD;fD=(558+fD);do local dN;dN=dG[1];dG[1]=cq[1];cq[1]=dN;dN=dJ;dJ=fs;fs=dN;end;fE=true;fF,fG=(fD-935)+(106585+935),42168+fD;fJ=fF;until aN[151]
	dL = ce(ct[1],aN[361][1][1],cq[1])
	bB = dL
	local dN
	cC[1] = {186}
	ci[1] = nil
	aY = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}
	fE = true
	fG = 1080493
	local dN
	cp[1] = dG[1]
	dG[1] = {186}
	dN = ""
	aW[1] = nil
	cj[1] = ""
	dN = 1
	cu[1] = {61, 205}
	aN[361][7][1] = 1
	fE = true
	fF,fG=801244+fD,fD+16390
	fE = true
	fF,fG=(fD-24)+(801244+24),20676+fD
	aN[361][2][1] = fR[1]
	aW[1] = nil
	cr[1] = aN[361][2][1][aW[1]]
	local dN
	dJ = nil
	aV = nil
	cq[1] = ""
	cj[1] = nil
	cl = nil
	dN = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}
	aY = 10067716
	aN[361][6][1] = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}
	dN = cn
	cn = nil
	ci[1] = dN
	dN = "gui"
	cf[1] = nil
	cA = "gui"
	fE = true
	fG = 1151012
	dJ = (if cr[1]then aN[24]~=349078 else aN[151])
	aN[361][4][1] = not dJ
	if not aN[361][4][1] then
	fD = 2399904
	do local dN;fs=cg[1];dN=dG[1];dG[1]=cm;cm=dN;dN=aV;aV=ci[1];ci[1]=dN;dN=co[1];co[1]=ck[1];ck[1]=dN;end
	fE = true
	fF = 3191664
	fG = 2395380
	fJ = 2807225
	else
	fD = 2391177
	cl,dC[1],ft[1],cg[1],cr[1],cm,fs,aX[1],dG[1],ck[1],dJ,ci[1],aV,co[1]=ft[1],cf[1],cl,ct[1],aX[1],dJ,cg[1],cr[1],cm,co[1],dG[1],aV,ci[1],ck[1]
	fE = true
	fF,fG=180555+fD,27630+fD
	fJ = 2807225
	end
	aW[1] = aN[24]==349078
	aN[361][2][1] = aW[1]
	cr[1] = fR[1]
	dJ = nil
	dJ = nil
	cr[1][dJ]=aN[361][2][1]
	aN[361][2][1] = fO[1]
	aW[1] = "R2"
	fE = true
	fF,fG=fD+180555,(fD-367)+(74019+367)
	aV = ""
	cx[1] = {100}
	cm = 6254731
	cn = 1
	aN[361][1][1] = {3940785, 1646321, 253, 169, 195}
	local dN
	dN = nil
	fr[1] = {26, 57, 144, 98, 77, 210, 139, 16, 61, 10, 78, 233, 56, 56, 204, 130, 26, 195, 120, 233, 117, 86, 90, 133, 230, 123, 123, 206, 254, 236, 51, 132, 218, 190, 71, 81, 215, 151, 183, 235, 103, 27, 24, 115, 169, 114, 85, 51, 131, 23, 191, 96, 77, 231, 149, 95, 157, 137, 249, 154, 159, 164, 9}
	fs = nil
	dN = 10141998
	ft[1] = ""
	aV = 10141998
	fE = true
	fF,fG=fD+15382,71455+fD
	ft[1] = "a"
	bv = "a"
	fE = true
	fF,fG=(fD-505)+(15382+505),fD+43078
	ft[1] = ""
	cn = 1
	cx[1] = {219, 25, 99, 252, 137, 227, 118, 168, 47, 243, 82, 200}
	aN[361][1][1] = {2741617, 786839, 33, 253, 135}
	dJ = 6770358
	fE = true
	fF,fG=fD+15382,(fD-254)+(70556+254)
	aN[1020] = aN[24]+671
	ft[1] = "SESSION_END:"
	hL = "SESSION_END:"
	local dN
	aX[1] = "gui"
	cA = cp[1]
	dN = 6770358
	dJ = {186}
	cf[1] = 6770358
	dN = {186}
	aY = aN[361][4][1]
	aN[361][4][1] = {186}
	fE = true
	fG = 1219637
	if hN==nil then
	ft[1] = ""
	cf[1] = 6746176
	cx[1] = {26, 115, 59, 121, 173, 90, 91, 158, 18, 171}
	cn = 1
	aN[361][1][1] = {1559401, 656963, 37, 203, 219}
	end
	fE = true
	fF,fG=(fD-277)+(821609+277),13375+fD
	if aN[24]==349078 then
	fD = 2395815
	co[1],cs[1],cl,cA,ch[1],aN[361][7][1],cx[1],ci[1],dL,aY,cf[1],ct[1],cr[1],cC[1]=aY,cf[1],co[1],cx[1],dJ,cr[1],cl,dL,ci[1],cA,ct[1],cs[1],aN[361][7][1],cj[1]
	fE = true
	fF,fG=fD+241708,fD+4388
	fJ = 2807225
	else
	aN[1050] = nil
	end
	local dN
	dJ = 10141998
	aW[1] = nil
	aV = 1
	dG[1] = 10067716
	dN = {186}
	co[1] = {219, 25, 99, 252, 137, 227, 118, 168, 47, 243, 82, 200}
	cx[1] = {186}
	dN = 6770358
	cf[1] = cg[1]
	cg[1] = 6770358
	dN = nil
	cp[1] = nil
	dC[1] = nil
	fE = true
	fF,fG=(fD-80)+(416805+80),16588+fD
	aN[361][6][1] = getfenv[fq]
	aN[361][3][1] = nil
	cq[1] = (if aN[24]==349078 then aN[361][6][1]else aN[362])(aN[361][3][1])
	local dN
	dN = nil
	dE = 10141998
	cl = nil
	dN = nil
	aW[1] = {186}
	aN[361][4][1] = nil
	fE = true
	fF,fG=fD+416805,6407+fD
	aX[1] = true
	aN[361][6][1] = {}
	aN[361][6][1] = true
	fE = true
	fG = 1233688
	aN[361][6][1] = getfenv[by]
	aN[361][3][1] = nil
	cq[1] = aN[361][6][1][(if aN[151]then aN[361][3][1]else aN)]
	local ik=cq[1]
	cx[1] = ik()
	fE = true
	fG = 1309160
	local dN
	aN[361][4][1] = nil
	dE = 10141998
	dN = nil
	cq[1] = cr[1]
	cr[1] = nil
	dN = {186}
	cm = nil
	cf[1] = aW[1]
	aW[1] = {186}
	fE = true
	fG = 1273915
	dE = (if aN[24]==349078 then ck[1]else aN[394])
	aX[1] = dE
	local dN
	cg[1] = dE
	dE = nil
	dN = {61, 205}
	cu[1] = aX[1]
	aX[1] = {61, 205}
	fE = true
	fG = 1300576
	local dN
	cs[1] = 10141998
	aX[1] = nil
	cl = {186}
	aW[1] = nil
	cr[1] = nil
	cm = nil
	aN[361][7][1] = nil
	aN[361][4][1] = nil
	fr[1] = cx[1]
	cx[1] = 10141998
	aN[361][5][1] = nil
	dC[1] = {219, 25, 99, 252, 137, 227, 118, 168, 47, 243, 82, 200}
	co[1] = 842907
	ck[1] = cg[1]
	cg[1] = "SESSION_END:"
	ft[1] = cu[1]
	cu[1] = dL
	dL = aN[361][6][1]
	dN = nil
	ci[1] = 1
	aV = 1
	cn = ch[1]
	ch[1] = 10067716
	dG[1] = nil
	cp[1] = cf[1]
	cf[1] = nil
	dN = 10067716
	cC[1] = aU
	aU = cq[1]
	cq[1] = ct[1]
	ct[1] = nil
	aY = nil
	cj[1] = 10067716
	fE = true
	fF,fG=fD+777839,fD+25810
	local dN
	fr[1] = 10067716
	aX[1] = ck[1]
	ck[1] = "SESSION_END:"
	cg[1] = cp[1]
	dN = nil
	ct[1] = {186}
	cl = nil
	fE = true
	fF,fG=1007925+fD,fD+2520
	local dN
	dN = nil
	aN[361][7][1] = {186}
	ct[1] = nil
	dN = 1
	ci[1] = dL
	dL = 1
	fE = true
	fF,fG=(fD-874)+(1007925+874),fD+48903
	cg[1] = 9
	ct[1] = (if aY>=cg[1]then aN[151]else aN[24]~=349078)
	cl = ct[1]
	aN[361][3][1] = cl
	cA = not ct[1]
	if not cA then
	fD = 2396273
	do local dN;ch[1]=aN[361][6][1];aN[361][6][1]=dJ;cp[1]=aW[1];dN=dE;dE=cq[1];cq[1]=dN;dN=co[1];co[1]=aY;aY=dN;dN=ct[1];ct[1]=cf[1];cf[1]=dN;dN=cr[1];cr[1]=aN[361][7][1];aN[361][7][1]=dN;end
	fE = true
	fF = 3251238
	fG = 2407196
	fJ = 2807225
	else
	fD = 2397344
	dJ,dE,cq[1],cp[1],aN[361][6][1]=aN[361][6][1],cq[1],dE,aW[1],dJ
	fE = true
	fF = 3907280
	fG = 2475577
	fJ = 2807225
	end
	dC[1] = (if aN[124]then aN[419]else aW[1])[(if not aN[124]then aN[361][3][1]else aN[387])]
	cC[1] = 2
	fs = cC[1]*aN[361][2][1]
	cm = 8387390
	cf[1] = 8387390
	fE = true
	fF,fG=fD+106585,1807+fD
	cp[1] = dC[1](fs,ch[1])
	ct[1] = cp[1]
	aN[361][2][1] = ct[1]
	fE = true
	fF,fG=(fD-420)+(1007925+420),(fD-406)+(87035+406)
	cm = 1
	aN[361][1][1] = {1138057, 2602509, 201, 189, 191}
	aW[1] = {39, 107, 45, 78}
	cp[1] = ""
	aU = 8373348
	local dN
	ft[1] = 10067716
	fs = cl
	dL = ""
	fr[1] = 10141998
	dN = {39, 107, 45, 78}
	aW[1] = ct[1]
	ct[1] = {39, 107, 45, 78}
	fE = true
	fG = 1451622
	if aN[24]==349078 then
	if fd==nil then dL=cc(ct[1],aN[361][1][1],aU);fd=dL;end
	fD = 2397031
	fD = 2393105
	do local dN;dN=dE;dE=dG[1];dG[1]=dN;end
	fE = true
	fF,fG=1951663+fD,fD+29908
	fJ = 2807225
	else
	aN[1033] = nil
	end
	aV = cc(cx[1],aN[361][1][1],cm)
	fn = aV
	local dN
	aU = 8387390
	dN = 10141998
	dJ = 10067716
	ft[1] = 10141998
	dN = ""
	cp[1] = dG[1]
	dG[1] = ""
	dN = 10067716
	cj[1] = 10067716
	aN[361][5][1] = 10067716
	fE = true
	fF,fG=fD+375161,(fD-921)+(88124+921)
	cm = 1991552
	cx[1] = {195, 164, 76, 175, 34, 96, 178, 59}
	dG[1] = 1
	aN[361][1][1] = {1775953, 470183, 73, 85, 145}
	aV = ""
	local dN
	co[1] = cl
	ct[1] = 10141998
	dN = nil
	aY = 8387390
	aU = nil
	fE = true
	fG = 1500822
	while aN[124]do aN[935]=aN[24];end
	aV = "authSent"
	eS = "authSent"
	fE = true
	fG = 1453284
	aN[908] = aN[24]+216
	return
	while aN[124]do aN[1005]=aN[24];end
	aY = ce(fr[1],aN[361][1][1],aX[1])
	bX = aY
	fE = true
	fF,fG=fD+1900168,fD+66457
	fs = 1
	cm = 10827727
	aY = ""
	fr[1] = {235}
	aN[361][1][1] = {3987373, 663295, 135, 159, 95}
	fE = true
	fG = 1478578
	aY = "c"
	bx = "c"
	local dN
	cl = 1991552
	dN = {195, 164, 76, 175, 34, 96, 178, 59}
	cx[1] = 10141998
	ft[1] = {195, 164, 76, 175, 34, 96, 178, 59}
	dN = co[1]
	co[1] = cp[1]
	cp[1] = dN
	fE = true
	fG = 1543515
	if hO==nil then
	fr[1] = {89, 128, 181, 131, 13, 208, 77, 187, 22, 6, 28, 128, 171, 234, 47, 31, 246}
	cm = 12442926
	aY = ""
	aN[361][1][1] = {2250385, 2721959, 187, 101, 253}
	fs = 1
	end
	fE = true
	fF,fG=(fD-406)+(548833+406),(fD-743)+(71006+743)
	ch[1] = "Y"
	eW = "Y"
	fE = true
	fG = 1527653
	if aN[24]==349078 then
	if bX==nil then fr[1]={7,240,(107-8)+8,215,(119-9)+9};cl=((fD+4005959)-(fD+596451));aY='';aX[1]=1;aN[361][1][1]={((fD+2298982)-(fD+57625)),((fD+2746656)-(fD+625875)),((fD+374056)-(fD+374045)),((fD+98923)-(fD+98912)),((fD+449038)-(fD+448857))};end
	fD = 2394687
	fD = 2398067
	aV,aN[361][6][1],ct[1],cC[1],ck[1],aX[1],cl=aN[361][6][1],aV,ck[1],cn,ct[1],cl,aX[1]
	fE = true
	fF = 4290588
	fG = 2467202
	fJ = 2807225
	else
	aN[982] = nil
	end
	aN[361][1][1] = {1138057, 2602509, 201, 189, 191}
	cm = 1
	cp[1] = ""
	aW[1] = {39, 107, 45, 78}
	aU = 8373348
	fE = true
	fG = 1555651
	dL = "math"
	fd = "math"
	local dN
	dN = nil
	dE = "authSent"
	dG[1] = nil
	fE = true
	fG = 1533356
	ci[1] = ce(cx[1],aN[361][1][1],cf[1])
	bw = ci[1]
	local dN
	cn = 10141998
	aU = 10067716
	cr[1] = co[1]
	ch[1] = "Y"
	aW[1] = 10067716
	dN = cu[1]
	cu[1] = nil
	aN[361][4][1] = dN
	fE = true
	fG = 1563065
	if eF==nil then
	ck[1] = 1
	cf[1] = 11380628
	cx[1] = {10, 253}
	ci[1] = ""
	aN[361][1][1] = {161773, 1520135, 141, 243, 57}
	end
	local dN
	co[1] = nil
	dN = cr[1]
	cr[1] = 1991552
	cl = dN
	dN = 10067716
	aW[1] = {39, 107, 45, 78}
	ct[1] = 10067716
	fE = true
	fG = 1599169
	aW[1] = nil
	local dN
	cA = ck[1]
	dN = 10067716
	cC[1] = ci[1]
	ci[1] = 10141998
	cx[1] = 10067716
	dN = 10067716
	ct[1] = cj[1]
	cj[1] = aX[1]
	aX[1] = 10067716
	fE = true
	fF,fG=fD+777839,(fD-472)+(30629+472)
	local dN
	ck[1] = "c"
	dJ = 10141998
	dE = "Y"
	dN = 10141998
	ci[1] = cC[1]
	cC[1] = cj[1]
	cj[1] = "Y"
	aY = ct[1]
	ct[1] = 10141998
	fE = true
	fF,fG=777839+fD,fD+8353
	fE = true
	fF,fG=fD+1007925,(fD-482)+(99303+482)
	cA = fW[1]
	aN[361][7][1] = "https://api.polsec.net/runtime/socket/heartbeat"
	dG[1] = nil
	dG[1] = (if aN[24]~=349078 then aN[379]else fC[1])
	cl = nil
	aN[361][3][1] = (if aN[24]==349078 then dG[1]else aN)[(if aN[24]==349078 then cl else aN[397])]
	aU = {}
	cr[1] = "a"
	fE = true
	fF,fG=1322618+fD,(fD-913)+(1905+913)
	while aN[124]do aN[901]=aN[24];end
	aN[361][5][1] = "restart"
	ft[1] = cq[1][aN[361][5][1]]
	dE = ft[1]
	ck[1] = dE
	fE = true
	fG = 1689367
	cp[1] = bZ(aW[1],aN[361][1][1],dC[1])
	bz = cp[1]
	local dN
	cC[1] = nil
	dN = 10141998
	dJ = 1991552
	cs[1] = 10141998
	dN = ck[1]
	ck[1] = "restart"
	aN[361][5][1] = aN[361][7][1]
	aN[361][7][1] = dN
	fE = true
	fF,fG=1594787+fD,5316+fD
	cp[1] = ""
	cm = 1
	aN[361][1][1] = {1000269, 2850955, 223, 209, 123}
	dC[1] = 15201458
	aW[1] = {139, 68, 140, 13, 76, 243, 8, 70}
	fE = true
	fG = 1679971
	aN[1062] = aN[24]+706
	cp[1] = "reported"
	fi = "reported"
	local dN
	cl = nil
	fr[1] = {}
	aU = 15201458
	dC[1] = "a"
	cr[1] = nil
	dN = 1991552
	cq[1] = 1991552
	ci[1] = 1991552
	fE = true
	fG = 1718472
	if aN[24]==349078 then
	if fl==nil then cx[1]=((fD+2803972)-(fD+341707));aN[361][1][1]={((fD+3732092)-(fD+157511)),((fD+2808027)-(fD+326704)),((fD+976532)-(fD+976525)),((fD+556230)-(fD+556041)),((fD+392035)-(fD+391814))};cA=1;ci[1]={(38+29)-29,(246-22)+22,213};aU='';end
	fD = 2392314
	fD = 2399007
	fs,aN[361][6][1],cp[1],cq[1],cs[1],cu[1],aW[1]=aW[1],cl,cu[1],cs[1],cq[1],cp[1],ci[1]
	fE = true
	fF = 3458005
	fG = 2467452
	fJ = 2807225
	else
	aN[1018] = nil
	end
	if fl==nil then
	aU = bZ(aW[1],aN[361][1][1],cx[1])
	fl = aU
	end
	fE = true
	fF,fG=816159+fD,(fD-573)+(54158+573)
	while aN[124]do aN[954]=aN[24];end
	if br==nil then
	aN[361][1][1] = {2327049, 1790831, 213, 151, 63}
	cA = 1
	ft[1] = 10393812
	aU = ""
	aW[1] = {61, 205}
	end
	fE = true
	fG = 1697636
	while aN[124]do aN[933]=aN[24];end
	if br==nil then
	aU = bZ(aW[1],aN[361][1][1],ft[1])
	br = aU
	end
	local dN
	cn = "reported"
	cl = "a"
	dC[1] = 10141998
	ft[1] = 15201458
	dN = dE
	dE = 1991552
	dJ = dN
	fE = true
	fG = 1673288
	if bB==nil then
	dL = ce(ct[1],aN[361][1][1],cq[1])
	bB = dL
	end
	local dN
	ci[1] = aY
	aY = cg[1]
	cC[1] = "a"
	fE = true
	fF,fG=676189+fD,(fD-191)+(27614+191)
	dL = bZ(aU,aN[361][1][1],cj[1])
	fh = dL
	local dN
	dG[1] = dL
	dN = "math"
	cu[1] = cj[1]
	cj[1] = "math"
	fE = true
	fF,fG=fD+1947707,(fD-460)+(77457+460)
	aN[361][2][1] = fh
	cf[1] = aN[361][2][1]~=cp[1]
	aN[361][6][1] = not cf[1]
	dE = aN[361][6][1]
	ch[1] = dE
	if 1 then
	fD = 2399277
	cA,cu[1],cq[1],cr[1]=cn,cr[1],aN[361][4][1],cu[1]
	fE = true
	fF,fG=1947707+fD,15115+fD
	fJ = 2807225
	else
	fD = 2395860
	cl,ct[1],cA,cu[1],cq[1],cj[1],aN[361][4][1],cr[1]=ct[1],cC[1],cn,cr[1],cj[1],aN[361][4][1],cf[1],cu[1]
	fE = true
	fF = 4132479
	fG = 2436853
	fJ = 2807225
	end
	local dN
	cn = 10067716
	ct[1] = "a"
	aN[361][4][1] = cf[1]
	dN = 1991552
	cq[1] = aN[361][6][1]
	aN[361][6][1] = "math"
	cj[1] = aN[361][7][1]
	aN[361][7][1] = 1991552
	dN = ch[1]
	ch[1] = 1991552
	aV = dN
	fE = true
	fG = 1823628
	repeat if eJ==nil then aU=cb(cg[1],aN[361][1][1],cx[1]);eJ=aU;end;fD=(fD+6094);fD=fD+5158;cn,cf[1],fr[1],aX[1],cl,dL,ft[1],cC[1],ci[1]=ft[1],aN[361][6][1],dL,cC[1],fr[1],cl,fs,aX[1],cg[1];fE=true;fF,fG=816159+fD,(fD-628)+(5123+628);fJ=fF;until aN[151]
	aX[1] = "request"
	local il=aN[361][2][1]
	dJ = il(aW[1],aU,ft[1],cp[1],dC[1],aX[1])
	local dN
	dN = ""
	cm = dJ
	dJ = ""
	dN = 15201458
	ft[1] = "a"
	cl = 15201458
	fE = true
	fG = 1765332
	aN[361][2][1] = (if aN[24]==349078 then aN else aN)
	aN[361][2][1] = (if aN[24]~=349078 then aN[392]else(139203+(-139198)))
	dJ = aN[361][2][1]~=cl
	aW[1] = (if dJ then not aN[151]else not aN[124])
	aN[361][4][1] = not aW[1]
	if not aN[361][4][1] then
	fD = 2395159
	cx[1],ct[1],co[1],cf[1],aU,cl,aX[1],dJ=aU,cl,ch[1],aX[1],cx[1],aN[361][6][1],dJ,co[1]
	fE = true
	fF = 2570975
	fG = 2488075
	fJ = 2807225
	else
	fD = 2391733
	do local dN;ct[1]=cl;cl=aN[361][6][1];dN=co[1];co[1]=aX[1];aX[1]=dN;dN=cx[1];cx[1]=aU;aU=dN;end
	fE = true
	fF,fG=180555+fD,(fD-442)+(71883+442)
	fJ = 2807225
	end
	local dN
	cf[1] = 1
	dE = aU
	aU = 15201458
	cx[1] = {}
	fr[1] = 10067716
	aN[361][5][1] = "a"
	aN[361][6][1] = 1991552
	aN[361][7][1] = dJ
	dJ = nil
	cn = aV
	aV = ci[1]
	ci[1] = nil
	cu[1] = "a"
	ft[1] = cg[1]
	cg[1] = dG[1]
	dG[1] = "reported"
	cA = aN[361][4][1]
	aN[361][4][1] = 10141998
	co[1] = 10141998
	dC[1] = "request"
	aX[1] = 1991552
	cs[1] = cj[1]
	cj[1] = aY
	aY = 15201458
	ct[1] = "math"
	cl = cq[1]
	cq[1] = cr[1]
	cr[1] = aW[1]
	aW[1] = "restart"
	ck[1] = cm
	fE = true
	fG = 1821106
	local dN
	ch[1] = cA
	dN = "a"
	cC[1] = {}
	cx[1] = "a"
	fE = true
	fF,fG=180555+fD,fD+77518
	while aN[124]do aN[972]=aN[24];end
	aW[1] = 1
	aN[361][2][1] = 1
	fE = true
	fG = 1823043
	if fq==nil then
	cg[1] = {251, 223, 74, 120}
	aN[361][1][1] = {2752569, 1202887, 71, 129, 153}
	ck[1] = 1
	aN[361][7][1] = 2567826
	aN[361][6][1] = ""
	end
	fE = true
	fF,fG=(fD-523)+(1238619+523),62598+fD
	if fq==nil then
	aU = cb(cg[1],aN[361][1][1],aN[361][7][1])
	fq = aU
	end
	local dN
	fs = "reported"
	dE = cs[1]
	dN = "math"
	ct[1] = cl
	cl = "math"
	dN = 1
	dL = 1
	cp[1] = 1
	fE = true
	fG = 1846577
	if bM==nil then
	cA = 1
	aN[361][1][1] = {1008365, 671311, 157, 215, 91}
	aU = ""
	cg[1] = {184, 130, 255, 242, 46, 206, 136}
	aN[361][7][1] = 6970858
	end
	fE = true
	fF,fG=1021813+fD,79222+fD
	if bM==nil then
	aU = cb(cg[1],aN[361][1][1],cx[1])
	bM = aU
	end
	fE = true
	fF,fG=fD+1021813,fD+71454
	aU = ""
	cA = 1
	cg[1] = {201, 202, 4, 10, 84, 73, 135, 41, 66, 186}
	aN[361][1][1] = {306169, 1287455, 63, 93, 59}
	cx[1] = 16310920
	local dN
	dG[1] = co[1]
	ct[1] = cr[1]
	cr[1] = cf[1]
	co[1] = nil
	dN = cu[1]
	cu[1] = "a"
	ch[1] = dN
	fE = true
	fF,fG=875988+fD,(fD-803)+(92209+803)
	cA = nil
	cA = (if not aN[124]then not aV else aN)
	if cA then
	fD = 2395311
	do local dN;fs=aN[361][7][1];dN=cx[1];cx[1]=dC[1];dC[1]=dN;end
	fE = true
	fF = 3104079
	fG = 2462772
	fJ = 2807225
	else
	fD = 2392839
	do local dN;cu[1]=dJ;aN[361][5][1]=ct[1];fs=aN[361][7][1];dN=cs[1];cs[1]=dE;dE=dN;dN=cx[1];cx[1]=dC[1];dC[1]=dN;end
	fE = true
	fF,fG=(fD-884)+(713659+884),fD+82170
	fJ = 2807225
	end
	fE = true
	fG = 1948564
	local dN
	aN[361][7][1] = cm
	dN = ci[1]
	ci[1] = nil
	cg[1] = dN
	dN = dE
	dE = nil
	fs = dN
	dN = 16310920
	aU = ""
	aN[361][4][1] = 16310920
	fE = true
	fG = 1926836
	aN[361][4][1] = {}
	cu[1] = "a"
	aV = 1
	(if aN[24]~=349078 then aN[405]else aN[361][4][1])[(if aN[151]then cu[1]else aN[370])]=aV
	cq[1] = bw
	cu[1] = cq[1]
	local im,hT,hU=aN[361][4][1],cu[1],cp[1]
	im[hT]=hU
	cu[1] = "c"
	(if not aN[124]then aN[361][4][1]else aN[368])[(if aN[24]~=349078 then aN[363]else cu[1])]=cx[1]
	cu[1] = bz
	aV = nil
	aV = 400
	(if not aN[124]then aN[361][4][1]else aN[389])[(if aN[124]then aN[423]else cu[1])]=aV
	cu[1] = bB
	aV = nil
	aV = (if aN[24]==349078 then eH else aN)
	aN[361][4][1][cu[1]]=aV
	fE = true
	fG = 2054461
	cu[1] = nil
	cu[1] = {}
	aV = nil
	aV = (if aN[24]~=349078 then aN[368]else fl)
	aN[361][3][1] = aN[361][6][1][(if not aN[124]then aV else aN[386])]
	cq[1] = 7010719
	aU = 7010719
	cC[1] = (if not aN[151]then aN else aN[361][3][1])(aN[361][6][1],aU)
	local io,ip,iq=aN[361][4][1],cu[1],cC[1]
	io[ip]=iq
	return 1
	aN[148] = getfenv
	aN[167] = string
	aN[15] = string.char
	fE = true
	fF,fG=fD+763790,fD+75157
	aN[105] = "format"
	aN[117] = string[aN[105]]
	fE = true
	fF,fG=763790+fD,(fD-44)+(89480+44)
	if bV==nil then
	cs[1] = ""
	cA = 1
	aN[361][1][1] = {3458321, 2841575, 197, 67, 171}
	fr[1] = {138, 204, 34, 77}
	aU = 7001144
	end
	local dN
	cp[1] = cC[1]
	aX[1] = nil
	aN[361][5][1] = nil
	aN[361][4][1] = nil
	dN = nil
	cs[1] = "math"
	cl = nil
	dN = 7010719
	fs = ch[1]
	ch[1] = "a"
	ct[1] = 7010719
	fE = true
	fF,fG=763790+fD,(fD-422)+(75412+422)
	if bV==nil then
	cl = ce(fr[1],aN[361][1][1],aU)
	bV = nil
	end
	fE = true
	fG = 2089346
	if by==nil then
	aU = 4755607
	aN[361][1][1] = {3511201, 455755, 53, 41, 221}
	fr[1] = {98, 190, 215, 31, 182, 120, 181, 148, 80}
	ck[1] = ""
	cA = 1
	end
	fE = true
	fF,fG=435336+fD,(fD-442)+(88613+442)
	cq[1] = 14
	cs[1] = false
	cx[1] = false
	aN[361][3][1] = (if aN[24]~=349078 then aN[368]else cx[1])
	fE = true
	fF,fG=241708+fD,fD+4388
	aY = not aN[361][3][1]
	if not aY then
	fD = 2399634
	do local dN;dN=ch[1];ch[1]=aV;aV=dN;end
	fE = true
	fF = 2632128
	fG = 2478216
	fJ = 2807225
	else
	fD = 2394736
	do local dN;aW[1]=ft[1];ft[1]=aN[361][5][1];cj[1]=cg[1];cg[1]=aN[361][6][1];aN[361][6][1]=cf[1];cf[1]=dG[1];dG[1]=cC[1];cm=cx[1];cx[1]=ct[1];ct[1]=co[1];co[1]=fr[1];dJ=ch[1];ch[1]=aV;aV=aN[361][7][1];dN=dE;dE=aX[1];aX[1]=dN;dN=fs;fs=dC[1];dC[1]=dL;dL=dN;end
	fE = true
	fF = 2807225
	fG = 2407008
	fJ = 2807225
	end
	cg[1] = {}
	dE = (if aN[24]~=349078 then aN[383]else aN[400])
	dE = (if aN[24]==349078 then bv else aN[416])
	aN[361][3][1] = (if aN[24]==349078 then aN else aN[368])
	aN[361][3][1] = nil
	cg[1][cf[1]]=(if aN[24]==349078 then aN[361][3][1]else aN[365])
	cf[1] = nil
	local ir,is,it=cg[1],cf[1],cs[1]
	ir[is]=it
	cf[1] = "c"
	cg[1][cf[1]]=cl
	dE = bz
	cf[1] = (if aN[24]==349078 then dE else aN[419])
	dE = 504
	local dN
	cj[1] = {}
	cg[1] = false
	dN = 1
	dL = 7010719
	fs = 1
	dN = 10141998
	co[1] = false
	ct[1] = 10141998
	fE = true
	fF,fG=241708+fD,fD+16678
	aN[361][3][1] = 504
	cj[1][cf[1]]=(if not aN[124]then aN[361][3][1]else aN)
	cf[1] = bB
	aN[361][3][1] = {}
	cq[1] = "a"
	co[1] = true
	aN[361][3][1][cq[1]]=co[1]
	dE = bw
	cq[1] = dE
	co[1] = (if aN[24]==349078 then hO else aN[374])
	(if aN[24]~=349078 then aN[401]else aN[361][3][1])[(if aN[24]~=349078 then aN else cq[1])]=co[1]
	fE = true
	fG = 2278659
	aU = fP[1]
	local iu=aU
	aN[361][5][1] = iu(cr[1],dL)
	aW[1] = nil
	aW[1] = (if aN[124]then aN[370]else not aN[361][5][1])
	if aW[1] then
	fD = 2390610
	do local dN;dE=cs[1];aN[361][6][1]=aN[361][5][1];dN=fr[1];fr[1]=ch[1];ch[1]=dN;dN=co[1];co[1]=cn;cn=dN;dN=fs;fs=ct[1];ct[1]=dN;end
	fE = true
	fF = 3112443
	fG = 2419805
	fJ = 2807225
	else
	fD = 2396584
	fr[1],aN[361][6][1],cA,ct[1],ch[1],cs[1],dE,fs,co[1],cn=ch[1],aN[361][5][1],ct[1],fs,fr[1],cm,cs[1],cA,cn,co[1]
	fE = true
	fF = 3711481
	fG = 2445702
	fJ = 2807225
	end
	local dN
	cs[1] = cn
	ck[1] = cf[1]
	cf[1] = ci[1]
	ci[1] = aU
	aU = aN[361][6][1]
	aN[361][5][1] = 7010719
	dL = aW[1]
	cn = dJ
	dJ = aN[361][7][1]
	aN[361][7][1] = cm
	dN = 1
	fs = 1
	cA = {}
	cj[1] = 1
	dN = nil
	co[1] = aX[1]
	aX[1] = nil
	fE = true
	fF,fG=1321061+fD,fD+35665
	fE = true
	fG = 2299461
	ci[1] = {}
	cu[1] = (if aN[24]~=349078 then aN[391]else bv)
	ci[1][cn]=aN[361][7][1]
	cn = bw
	local iv,iw,ix=ci[1],cn,cp[1]
	iv[iw]=ix
	cn = (if aN[24]~=349078 then aN else aN[403])
	cn = "c"
	ci[1][cn]=dC[1]
	cn = bz
	ci[1][cn]=cr[1]
	cu[1] = bB
	cn = cu[1]
	local iy,iz,iA=ci[1],cn,aN[361][5][1]
	iy[iz]=iA
	fE = true
	fF,fG=fD+1321061,75424+fD
	return {}
	fE = true
	fF,fG=1321061+fD,(fD-429)+(35665+429)
	aU = (if aN[24]~=349078 then aN[400]else aN)
	aU = nil
	cl = (if aN[24]~=349078 then aN[375]else aN[404])
	cl = nil
	dJ = true
	aN[361][7][1] = true
	aV = true
	local dN
	aN[361][6][1] = aN[361][5][1]
	aN[361][4][1] = 1
	cm = cq[1]
	cq[1] = cu[1]
	dN = dL
	dL = {}
	cA = dN
	dN = cf[1]
	cf[1] = 1
	cj[1] = dN
	fE = true
	fF,fG=1054614+fD,90852+fD
	aN[361][3][1] = nil
	aN[361][6][1] = cC[1][(if aN[24]~=349078 then aN[418]else aN[361][3][1])]
	cu[1] = not aN[361][6][1]
	cg[1] = cu[1]
	ct[1] = (if aN[124]then aN[386]else cg[1])
	fE = true
	fG = 2390224
	local iB,iC,iD=cj[1],cf[1],aN[361][3][1]
	iB[iC]=iD
	return cj[1]
	fE = true
	fG = 2480563
	-- region end
	-- warn: no leaf for key (763790, 1377406)
	-- warn: repeat-until 'aN[151]' not pre-true; one-shot assumed
	-- warn: repeat-until 'aN[151]' not pre-true; one-shot assumed
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @62136
	aU = aS
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @64204
	return hJ(aN[534][11],fu,fv,aN[534][14],aN[534][6],aW,aN[534][5],fw,aN[534][4],aN[534][2],aX,dJ,aY,fx,aN[534][18],ck,aN[534][17],aN[534][12],cu,dC,aN[534][9],cm,co,cC,cx,dE,...)end
	aN[534][5][1] = nil
	fD = 272859
	dL[1] = function(...)local hp=function(...)
	-- for-dispatch over iE=370..574 step 6
	aN = {}
	aN[818] = 4486
	aH = 1309
	aM = true
	aN[(394-394)+876]=394+5849
	aN[(836+233)-233]=400+5014
	aN[111] = true
	aN[412+217]=412~=556
	aN[865] = 7592
	aN[(673+295)-295]=430~=562
	aN[(607+459)-459]=436+6893
	aN[669] = 7294
	aN[448+273]=448+1901
	aN[708] = 6223
	aN[765] = 7082
	aN[472+229]=472~=532
	aN[478+145]=478+1668
	aN[484+118]=484+4751
	aN[490-374]=false
	aN[496+361]=496+8843
	aN[502+247]=502+6805
	aN[(782+126)-126]=508+4057
	aN[(875+209)-209]=514+3827
	aN[(609+380)-380]=520+6853
	aN[526+322]=526+1447
	aN[209] = 291982
	aN[538+180]=538+1869
	aN[(830+112)-112]=544+8449
	aN[(550-550)+636]=550+9701
	aN[556+158]=556+7180
	aK = function(...)
	ct[1] = gg
	aN[395][17][1] = gh
	aV[1] = gi
	dL[1] = gj
	aN[395][24][1] = gk
	aN[80] = getfenv
	aN[58] = string
	aN[15] = string.char
	fE = true
	aN[74] = "format"
	aN[90] = string[aN[74]]
	fE = true
	while aN[116]do aN[996]=aN[209];end
	cl = 5272243
	cm[1] = {811333, 2798249, 15, 19, 69}
	cn[1] = {209, 23, 211, 88, 184}
	aN[395][8][1] = ""
	cf = 1
	local dN
	dN = 5272243
	cl = nil
	cx = 5272243
	fE = true
	aN[395][8][1] = "clock"
	eU = "clock"
	local dN
	aN[395][27][1] = nil
	aN[395][26][1] = nil
	fr[1] = nil
	cC = 1
	aY[1] = nil
	dN = nil
	ft = nil
	cp[1] = nil
	fE = true
	cm[1] = {3900049, 2279877, 133, 117, 179}
	cx = 13238410
	cC = 1
	cn[1] = {239, 173}
	aN[395][8][1] = ""
	fE = true
	aN[395][8][1] = "R2"
	br = "R2"
	fE = true
	cn[1] = {37, 89, 38, 133, 161, 200}
	aY[1] = 9199125
	cm[1] = {510601, 2269061, 61, 47, 247}
	cC = 1
	aN[395][8][1] = ""
	fE = true
	aN[395][8][1] = "insert"
	fb = "insert"
	fE = true
	aN[395][26][1] = {65, 40, 126, 121, 117, 237, 86, 76}
	aN[395][8][1] = ""
	dJ[1] = {3404173, 1546387, 167, 173, 123}
	cC = 1
	cn[1] = 2690171
	local dN
	cf = 2690171
	dN = nil
	cj = nil
	cp[1] = nil
	dN = nil
	cg[1] = dC[1]
	dC[1] = nil
	fE = true
	aN[395][8][1] = "terminal"
	fn = "terminal"
	local dN
	dN = nil
	aN[395][25][1] = nil
	cx = nil
	fE = true
	cf = 13229291
	aN[395][26][1] = {173, 41, 108, 28}
	aN[395][8][1] = ""
	dJ[1] = {3396361, 2260625, 245, 221, 193}
	cC = 1
	local dN
	cm[1] = nil
	dC[1] = nil
	dN = nil
	co[1] = nil
	fr[1] = nil
	fE = true
	aN[395][8][1] = "math"
	fd = "math"
	local dN
	cu[1] = nil
	cn[1] = 13229291
	dN = aW
	aW = nil
	co[1] = dN
	fE = true
	cn[1] = 14688890
	aN[395][26][1] = {178, 208, 22, 189}
	cC = 1
	dJ[1] = {2236017, 3494159, 159, 181, 155}
	aN[395][8][1] = ""
	local dN
	cf = nil
	cl = nil
	dN = aN[395][27][1]
	aN[395][27][1] = {2236017, 3494159, 159, 181, 155}
	dJ[1] = dN
	fE = true
	aN[395][8][1] = "http"
	bI = "http"
	local dN
	dN = 1
	cC = nil
	cp[1] = 1
	dN = nil
	cf = {178, 208, 22, 189}
	aN[395][26][1] = nil
	fE = true
	aN[395][27][1] = {2916621, 1158297, 221, 145, 245}
	cn[1] = 4229226
	aN[395][8][1] = ""
	cf = {142, 21, 46, 1, 212, 220, 140, 63, 56, 92, 26, 105, 6, 11, 177, 8, 211, 108, 17, 209, 6, 204, 126, 11, 80, 174, 107, 224, 48, 182, 123, 72, 40, 173, 159, 9, 152, 137, 211, 12, 116, 31}
	cp[1] = 1
	fE = true
	aN[395][8][1] = "https://api.polsec.net/runtime/socket/http"
	eZ = "https://api.polsec.net/runtime/socket/http"
	fE = true
	aN[395][27][1] = {685281, 788389, 69, 25, 59}
	cn[1] = 14749226
	cf = {20}
	cg[1] = 1
	aN[395][8][1] = ""
	local dN
	dN = nil
	aW = 14749226
	cn[1] = nil
	dN = nil
	cl = nil
	fr[1] = nil
	fE = true
	aN[395][8][1] = "b"
	bw = "b"
	local dN
	aN[395][28][1] = nil
	dN = 1
	cg[1] = nil
	fr[1] = 1
	fE = true
	aN[395][27][1] = {754021, 1725939, 121, 149, 179}
	fr[1] = 1
	aN[395][8][1] = ""
	cf = {233, 30, 2, 60, 8}
	aW = 7559871
	fE = true
	aN[395][8][1] = "table"
	fm = "table"
	fE = true
	aN[395][8][1] = ""
	cx = {3535237, 488535, 27, 227, 15}
	aW = 6734990
	cf = {129, 94, 41, 158}
	fr[1] = 1
	fE = true
	aN[395][8][1] = "last"
	fc = "last"
	fE = true
	while aN[116]do aN[1029]=aN[209];end
	aW = 12902115
	aN[395][8][1] = ""
	cf = {113, 200, 4, 254}
	cx = {2059717, 2965217, 187, 187, 167}
	fr[1] = 1
	fE = true
	aN[395][8][1] = "1003"
	eD = "1003"
	fE = true
	aW = 7725756
	cf = {81, 123, 250, 222, 110, 252, 69, 196}
	fr[1] = 1
	cx = {3124417, 838319, 207, 119, 63}
	aN[395][8][1] = ""
	fE = true
	aN[1089] = 292070
	aN[395][8][1] = "inflight"
	fa = "inflight"
	local dN
	dN = cn[1]
	cn[1] = nil
	cp[1] = dN
	dN = nil
	ft = nil
	dG = cr[1]
	cr[1] = nil
	fE = true
	aN[395][8][1] = ""
	fr[1] = 1
	cA = 683394
	cx = {2757085, 290473, 249, 227, 219}
	cf = {88, 98, 198, 110, 194, 132, 141}
	fE = true
	aN[395][8][1] = "timeout"
	iK = "timeout"
	local dN
	dN = nil
	cn[1] = nil
	aN[395][28][1] = 683394
	cA = nil
	fE = true
	while aN[116]do aN[1019]=aN[209];end
	if bQ==nil then
	aN[395][28][1] = 14985039
	fr[1] = 1
	cf = {10, 254, 113, 158, 23, 191}
	aN[395][8][1] = ""
	dC[1] = {3207497, 2548141, 247, 97, 177}
	end
	local dN
	cm[1] = nil
	cx = {2757085, 290473, 249, 227, 219}
	dN = {88, 98, 198, 110, 194, 132, 141}
	cf = nil
	ft = {88, 98, 198, 110, 194, 132, 141}
	dN = nil
	aW = 1
	fr[1] = nil
	fE = true
	if bQ==nil then
	aN[395][8][1] = bZ(ft,cx,aN[395][28][1])
	bQ = "rejected"
	end
	fE = true
	aN[1007] = 292584
	cx = {1190213, 1999771, 87, 125, 121}
	aN[395][8][1] = ""
	aW = 1
	aN[395][28][1] = 5445954
	ft = {75, 27}
	fE = true
	aN[395][8][1] = "os"
	fg = "os"
	local dN
	dN = nil
	fr[1] = nil
	dG = nil
	dN = nil
	cr[1] = nil
	co[1] = nil
	dN = aN[395][26][1]
	aN[395][26][1] = nil
	cp[1] = dN
	fE = true
	repeat if iG==nil then aN[395][8][1]='';aW=1;cx={((fD+675461)-(fD+635708)),((fD+3585079)-(fD+165604)),((fD+909441)-(fD+909280)),((fD+657626)-(fD+657585)),((fD+689565)-(fD+689442))};ft={226,30,115,243};aN[395][28][1]=((fD+5921213)-(fD+126888));end;fD=fD+8958;fD=(1184+fD);do local dN;cC=dG;dG=cr[1];dN=cA;cA=cj;cj=dN;dN=cp[1];cp[1]=cf;cf=dN;end;fE=true;fF=(fD-525)+(1175534+525);fG=36042+fD;fJ=fF;until aN[111]
	fE = true
	co[1] = nil
	aN[395][22][1] = nil
	aN[395][15][1] = aN[395][7][1][aN[395][22][1]]
	aN[395][6][1] = 1
	cj = aN[395][15][1]~=aN[395][6][1]
	cx = not cj
	ft = (if aN[111]then cx else aN)
	aN[395][25][1] = ft
	while aN[116]do aN[1080]=aN[209];end
	fE = true
	cq = 1
	aN[395][13][1] = 1
	aN[395][16][1] = (if aW then aN[116]else aN[209]==291982)
	if not aN[395][16][1] then
	fD = 2977450
	do local dN;cn[1]=dE[1];dN=cf;cf=cj;cj=aX[1];aX[1]=aN[395][28][1];aN[395][28][1]=dN;dN=aN[395][26][1];aN[395][26][1]=cu[1];cu[1]=dN;end
	fE = true
	fF = 3133572
	fG = 3019740
	fJ = 3449692
	else
	fD = 2976610
	do local dN;cn[1]=dE[1];dN=aN[395][28][1];aN[395][28][1]=cf;cf=dN;end
	fE = true
	fF = 3133572
	fG = 3061828
	fJ = 3449692
	end
	aN[395][20][1] = 1901
	cl = (if aN[395][10][1]~=aN[395][20][1]then aN[209]==291982 else aN[116])
	aN[395][12][1] = not cl
	cq = aN[395][12][1]
	aN[395][13][1] = (if aN[116]then aN[432]else cq)
	fE = true
	aN[395][14][1] = aN[395][13][1]
	aN[395][16][1] = (if aN[395][13][1]then aN[116]else aN[111])
	if not aN[395][16][1] then
	fD = 2978948
	cu[1],cg[1],dJ[1],cr[1],co[1],ft=co[1],ft,cr[1],aN[395][25][1],cu[1],cg[1]
	fE = true
	fF = 4073263
	fG = 3073011
	fJ = 3449692
	else
	fD = 2976229
	dJ[1],cr[1]=cr[1],aN[395][25][1]
	fE = true
	fF = 3133572
	fG = 3027451
	fJ = 3449692
	end
	cx = 1904
	fr[1] = (if cx==aN[395][10][1]then aN[111]else aN[116])
	aN[395][14][1] = fr[1]
	local dN
	dN = cu[1]
	cu[1] = nil
	co[1] = dN
	dN = nil
	ft = cg[1]
	cg[1] = nil
	fE = true
	fE = true
	aN[395][10][1] = (if aN[116]then aN[420]else getfenv[fm])
	co[1] = "insert"
	aN[395][25][1] = aN[395][10][1][co[1]]
	dE[1] = nil
	dE[1] = (if not aN[116]then fS[1]else aN[414])
	cn[1] = nil
	local gW,gX=dE[1],cn[1]
	aX[1] = gW[gX]
	local gR=aN[395][25][1]
	cx = gR(aX[1],aN[395][11][1])
	aN[395][27][1] = {}
	aN[395][27][1] = nil
	aN[395][10][1] = nil
	local iM,iN=cs[1],aN[395][10][1]
	co[1] = iM[iN]
	aN[395][25][1] = 2
	dE[1] = co[1]==aN[395][25][1]
	local dN
	dN = nil
	aN[395][28][1] = cx
	cx = nil
	fE = true
	aW = (if aN[209]~=291982 then aN else ge[1])
	aN[395][26][1] = "R2"
	aN[395][27][1] = nil
	return aW(aN[395][26][1],aN[395][27][1],aN[395][17][1],aN[395][11][1],ct[1])
	local dN
	cu[1] = nil
	aX[1] = aW
	dN = cq
	cq = nil
	cn[1] = dN
	dN = nil
	dJ[1] = nil
	cg[1] = nil
	dN = nil
	cp[1] = fr[1]
	fr[1] = nil
	fE = true
	fE = true
	return cs[1]
	cC = getfenv[bV]
	local iO=(if aN[116]then aN[456]else cC)
	cr[1] = iO(ch[1])
	aX[1] = {}
	aX[1] = "string"
	aN[395][28][1] = cr[1]==aX[1]
	dE[1] = aN[395][28][1]
	aN[395][10][1] = nil
	aN[395][10][1] = (if aN[116]then aN[440]else dE[1])
	local dN
	ft = dE[1]
	dN = nil
	cq = aW
	aW = nil
	fE = true
	aN[395][16][1] = not aN[395][10][1]
	aN[395][10][1] = nil
	dE[1] = {}
	dE[1] = 5
	co[1] = 5
	cx = co[1]==aN[395][17][1]
	aN[395][27][1] = cx
	aW = aN[395][27][1]
	if ",\"d\":" then
	fD = 2977547
	do local dN;dN=cr[1];cr[1]=cj;cj=dN;dN=fr[1];fr[1]=aN[395][27][1];aN[395][27][1]=dN;end
	fE = true
	fF = 2986353
	fG = 2981699
	fJ = 3449692
	else
	fD = 2978213
	do local dN;dN=dG;dG=cq;cq=dN;dN=cu[1];cu[1]=cf;cf=dN;dN=cl;cl=aN[395][26][1];aN[395][26][1]=dN;dN=cr[1];cr[1]=cj;cj=dN;dN=fr[1];fr[1]=aN[395][27][1];aN[395][27][1]=dN;end
	fE = true
	fF = 2986353
	fG = 3052573
	fJ = 3449692
	end
	local dN
	dN = cx
	cx = ft
	ft = dN
	dN = cq
	cq = fr[1]
	fr[1] = nil
	dG = dN
	dN = nil
	cu[1] = {2757085, 290473, 249, 227, 219}
	cf = nil
	dN = "R2"
	aN[395][26][1] = cl
	cl = "R2"
	fE = true
	local dN
	dN = aW
	aW = nil
	fr[1] = dN
	dN = ft
	ft = cx
	cx = dN
	fE = true
	fE = true
	cC = getfenv[bV]
	local iP=(if aN[209]==291982 then cC else aN[449])
	cj = iP(aN[395][7][1])
	aX[1] = "table"
	local dN
	dN = cl
	cl = "R2"
	aN[395][28][1] = dN
	dN = cn[1]
	cn[1] = 5
	cq = co[1]
	co[1] = dN
	fE = true
	cx = aX[1]~=cj
	cl = (if cx then aN[116]else not aN[116])
	ft = cl
	aN[395][10][1] = ft
	fE = true
	repeat ft=aN[395][10][1];fD=(4403+fD);cp[1]=(if aN[209]~=291982 then aN[435]else aN[457]);cp[1]=(if aN[209]==291982 then ft else aN[398]);fD=(fD+2426);if aN[395][10][1]then fD=(5029+fD);cg[1],cr[1],fr[1],cl,cf=cC,cl,cf,cr[1],aY[1];fE=true;fF,fG=587689+fD,(fD-468)+(6701+468);fJ=fF;else fD=491+fD;cA,cj,cr[1],fr[1],cl,cg[1],cf=cC,cA,cl,cf,cr[1],cj,aY[1];fE=true;fF,fG=fD+851473,84244+fD;fJ=fF;end;until aN[111]
	if bV==nil then
	aN[395][8][1] = cb(aY[1],fr[1],aN[395][28][1])
	bV = "rejected"
	end
	fE = true
	aN[395][27][1] = 1
	aN[395][8][1] = ""
	aN[395][28][1] = 12275526
	fr[1] = {2698125, 1152795, 107, 143, 147}
	aY[1] = {225, 77, 183, 43, 234, 169, 145, 195, 4, 77}
	local dN
	co[1] = 1
	aN[395][27][1] = dG
	dN = "table"
	aX[1] = {225, 77, 183, 43, 234, 169, 145, 195, 4, 77}
	aY[1] = "table"
	dN = nil
	cm[1] = cl
	cl = nil
	fE = true
	while aN[116]do aN[1033]=aN[209];end
	aN[395][8][1] = "JSONEncode"
	eJ = "JSONEncode"
	local dN
	aN[395][26][1] = cm[1]
	dG = nil
	dN = 5
	cn[1] = {2698125, 1152795, 107, 143, 147}
	fr[1] = 5
	dN = nil
	cl = cr[1]
	cr[1] = nil
	fE = true
	aN[1049] = 292046
	aN[395][8][1] = ""
	cn[1] = {654257, 3805441, 117, 127, 129}
	aN[395][28][1] = 3652800
	co[1] = 1
	aX[1] = {110, 82, 107, 234}
	fE = true
	aN[395][8][1] = bZ(cg[1],cx,aN[395][28][1])
	bz = aN[395][8][1]
	fE = true
	repeat if eT==nil then aX[1]={((fD+2065122)-(fD+989145)),((fD+2540448)-(fD+253277)),((fD+809988)-(fD+809885)),((fD+217027)-(fD+216928)),((fD+489637)-(fD+489582))};cg[1]={87,(246-13)+13,75};dE[1]=1;aN[395][28][1]=((fD+15345057)-(fD+35366));aN[395][8][1]='';end;fD=(3266+fD);fD=(7288+fD);aN[395][25][1],cA,cf,aW,aN[395][27][1],cj=aW,cf,cA,aN[395][25][1],fr[1],dC[1];fE=true;fF=1954290+fD;fG=fD+69434;fJ=fF;until aN[111]
	fE = true
	aN[395][22][1] = fW[1]
	aN[395][15][1] = 0.75
	aN[395][6][1] = getfenv[fd]
	aN[395][28][1] = nil
	dJ[1] = nil
	dJ[1] = nil
	cf = aN[395][6][1][(if aN[209]==291982 then dJ[1]else aN[426])]
	aN[395][5][1] = (if not aN[111]then aN else cf)()
	cA = 0.5
	aN[395][27][1] = aN[395][5][1]*cA
	cn[1] = nil
	cn[1] = (if not aN[111]then aN[448]else aN[395][15][1]+aN[395][27][1])
	aN[395][3][1] = (if not aN[116]then cn[1]*ck[1]else aN[400])
	local iQ=(if aN[209]~=291982 then aN[448]else aN[395][22][1])
	aN[395][21][1] = iQ(aN[395][3][1],dL[1])
	aN[395][15][1] = getfenv[fd]
	aN[395][6][1] = nil
	dJ[1] = (if aN[209]==291982 then aN[395][15][1]else aN)[(if aN[209]==291982 then aN[395][6][1]else aN[451])]
	cf = 2
	fE = true
	aN[395][5][1] = cf*ck[1]
	cA = 8
	aN[395][22][1] = dJ[1](aN[395][5][1],cA)
	aX[1] = (if not aN[116]then aN[395][22][1]else aN[425])
	ck[1] = aX[1]
	fE = true
	local dN
	ft = nil
	aW = 8
	cj = dJ[1]
	cm[1] = aN[395][27][1]
	aN[395][27][1] = {110, 82, 107, 234}
	cx = 5
	cl = "table"
	cA = {2757085, 290473, 249, 227, 219}
	cu[1] = 2
	cf = nil
	aN[395][26][1] = 1
	co[1] = cC
	cg[1] = fr[1]
	fr[1] = cn[1]
	cn[1] = cp[1]
	cp[1] = nil
	cC = cq
	cq = dG
	dG = dE[1]
	dE[1] = nil
	dN = aX[1]
	aX[1] = aN[395][25][1]
	aN[395][25][1] = dN
	fE = true
	aN[1087] = 292373
	aN[395][22][1] = nil
	aN[395][22][1] = 1
	cl = aN[395][22][1]~=aN[395][17][1]
	aN[395][15][1] = not cl
	aN[395][16][1] = not aN[395][15][1]
	dJ[1] = 202
	cC = 202
	cj = cC==aN[395][2][1]
	aN[395][19][1] = not cj
	aN[395][16][1] = (if aN[395][19][1]then not aN[111]else aN[209]==291982)
	cC = gb[1]
	local iR=cC
	aN[395][19][1] = iR(ci[1])
	fE = true
	aN[395][8][1] = cc(aN[395][26][1],cu[1],aN[395][25][1])
	fl = aN[395][8][1]
	local dN
	cn[1] = aN[395][25][1]
	dN = 8
	aW = nil
	dC[1] = 8
	dN = cg[1]
	cg[1] = fr[1]
	fr[1] = dN
	fE = true
	cu[1] = {1142405, 3783405, 225, 71, 97}
	co[1] = 1
	aN[395][8][1] = ""
	cn[1] = 895395
	aN[395][26][1] = {244, 204, 224}
	local dN
	cf = {1142405, 3783405, 225, 71, 97}
	dN = 895395
	cn[1] = cr[1]
	cr[1] = 895395
	dN = 8
	dC[1] = fr[1]
	fr[1] = 8
	fE = true
	aN[395][8][1] = "min"
	fe = "min"
	fE = true
	cr[1] = 3222112
	cm[1] = 1
	aN[395][26][1] = {16}
	cf = {2132813, 3994521, 181, 163, 155}
	aN[395][8][1] = ""
	fE = true
	cu[1] = bz
	local fL,fM=cs[1],cu[1]
	aN[395][27][1] = fL[fM]
	cp[1] = nil
	cp[1] = 500
	aN[395][19][1] = cp[1]<=aN[395][27][1]
	aW = aN[395][19][1]
	fr[1] = (if aN[116]then aN[410]else aW)
	local dN
	dN = aW
	aW = fr[1]
	fr[1] = cq
	cq = dN
	fE = true
	if bb==nil then
	aN[395][8][1] = "/ÉRµà\5Ò³"
	bb = "rejected"
	end
	local dN
	aN[395][26][1] = fr[1]
	dN = nil
	ft = aY[1]
	aY[1] = nil
	dN = aX[1]
	aX[1] = aN[395][25][1]
	aN[395][25][1] = dN
	fE = true
	aN[957] = 292634
	co[1] = 1
	aN[395][25][1] = 7568054
	aN[395][8][1] = ""
	cu[1] = {3285885, 1633817, 229, 127, 113}
	aN[395][26][1] = {153, 254, 250, 94, 104, 30, 77, 247}
	fE = true
	aN[395][8][1] = "answered"
	eR = "answered"
	local dN
	cl = nil
	dE[1] = fr[1]
	dN = cm[1]
	cm[1] = {2132813, 3994521, 181, 163, 155}
	aY[1] = 5
	cx = dN
	dN = {110, 82, 107, 234}
	cA = 202
	cg[1] = {110, 82, 107, 234}
	fE = true
	if fl==nil then
	aN[395][26][1] = {20, 236, 120}
	aN[395][25][1] = 14682314
	aN[395][8][1] = ""
	co[1] = 1
	cu[1] = {1400513, 1706043, 165, 143, 65}
	end
	local dN
	fr[1] = ft
	dN = 2
	aN[395][27][1] = {110, 82, 107, 234}
	cg[1] = 2
	fE = true
	while aN[116]do aN[1002]=aN[209];end
	local dN
	cC = 5
	cr[1] = dC[1]
	dN = dE[1]
	dE[1] = cn[1]
	cn[1] = dN
	fE = true
	aN[395][11][1] = fS[1]
	aN[395][1][1] = nil
	ck[1] = (if aN[209]~=291982 then aN else aN[395][11][1])[(if not aN[111]then aN[418]else aN[395][1][1])]
	fs[1] = 1
	ci[1] = fs[1]+ck[1]
	aN[395][11][1][aN[395][1][1]]=(if aN[209]==291982 then ci[1]else aN)
	aN[395][1][1] = nil
	aN[395][1][1] = (if aN[209]~=291982 then aN[395]else fS[1])
	ck[1] = nil
	local iS,iT=aN[395][1][1],ck[1]
	fs[1] = iS[iT]
	aN[395][11][1] = fs[1]
	ck[1] = (if not aN[116]then fP[1]else aN)
	fs[1] = "JSONEncode"
	local iU,iV=ck[1],fs[1]
	ci[1] = iU[iV]
	aU[1] = {}
	local dN
	dN = 202
	cA = 7568054
	aN[395][25][1] = 202
	fE = true
	aN[395][8][1] = bZ(aX[1],cn[1],aN[395][28][1])
	eX = aN[395][8][1]
	local dN
	aN[395][25][1] = {110, 82, 107, 234}
	dN = cx
	cx = cr[1]
	cr[1] = dN
	fE = true
	cn[1] = {3248597, 3213079, 151, 37, 95}
	aX[1] = {189, 123, 77, 134, 223}
	aN[395][8][1] = ""
	aN[395][28][1] = 5127837
	co[1] = 1
	local dN
	cm[1] = dE[1]
	dE[1] = dG
	dN = ft
	ft = {3248597, 3213079, 151, 37, 95}
	cn[1] = dN
	fE = true
	aN[1005] = 292208
	aN[395][8][1] = "pcall"
	bK = "pcall"
	fE = true
	cl = {412197, 3748527, 213, 183, 181}
	aN[395][28][1] = 12486986
	aX[1] = {249, 11, 148, 179, 186, 215, 172}
	co[1] = 1
	aN[395][8][1] = ""
	local dN
	cr[1] = 500
	aN[395][27][1] = 2
	cg[1] = 1
	dN = aW
	aW = cn[1]
	cn[1] = dN
	dN = {249, 11, 148, 179, 186, 215, 172}
	aX[1] = cj
	cj = {249, 11, 148, 179, 186, 215, 172}
	fE = true
	local dN
	cC = aW
	aN[395][27][1] = cn[1]
	cn[1] = dE[1]
	dE[1] = 7568054
	cA = fr[1]
	aW = 500
	fr[1] = {153, 254, 250, 94, 104, 30, 77, 247}
	cu[1] = nil
	cf = 5
	aY[1] = dC[1]
	dC[1] = {3285885, 1633817, 229, 127, 113}
	dN = 500
	dG = {249, 11, 148, 179, 186, 215, 172}
	cj = cq
	cq = 1
	co[1] = 1
	dJ[1] = 500
	dN = aX[1]
	aX[1] = {110, 82, 107, 234}
	aN[395][25][1] = 500
	cp[1] = dN
	fE = true
	while aN[116]do aN[996]=aN[209];end
	aN[395][5][1] = nil
	dC[1] = false
	fr[1] = true
	cr[1] = true
	fE = true
	cr[1] = 5
	aN[395][15][1] = 5
	local dN
	cA = 7568054
	dE[1] = 1
	dN = aN[395][27][1]
	aN[395][27][1] = ft
	ft = dN
	dN = aY[1]
	aY[1] = {412197, 3748527, 213, 183, 181}
	cl = dN
	fE = true
	fE = true
	co[1] = getfenv[bV]
	aN[395][25][1] = nil
	aY[1] = cs[1][(if aN[111]then aN[395][25][1]else aN)]
	cn[1] = co[1](aY[1])
	aX[1] = "table"
	cx = nil
	cx = (if aN[209]==291982 then aX[1]==cn[1]else aN[413])
	local dN
	fr[1] = aN[395][27][1]
	cl = false
	dN = aY[1]
	aY[1] = 500
	aW = dN
	fE = true
	while aN[116]do aN[1001]=aN[209];end
	dJ[1] = cx
	aN[395][19][1] = dJ[1]
	fE = true
	local dN
	cf = cn[1]
	dN = {3285885, 1633817, 229, 127, 113}
	cC = aN[395][26][1]
	aN[395][26][1] = {3285885, 1633817, 229, 127, 113}
	dN = nil
	dG = {249, 11, 148, 179, 186, 215, 172}
	aN[395][25][1] = nil
	dN = 7568054
	cp[1] = cx
	cx = 7568054
	fE = true
	repeat aN[395][10][1]=getfenv[bK];fD=9070+fD;cC=(function(iW,iX,iY,iZ,je,jf,jg,jh,ji,jj,jk,jl,jm,jn,jo,jp,jq,jr,js,jt,jw,jx,jy,jz,jA,jB,jC,jD,jG,jH,jI,jJ,hp,jK,jL,jM,jN,jO,jP,jQ,jW)return function(...)return(function(...)
	-- for-dispatch over jX=888..828 step -2
	aH = 1
	aH = 0
	aN = {}
	aN[(805+468)-468]=882+5759
	aH = 1146
	aM = true
	aN[876-723]=308211
	aN[(842+424)-424]=874~=878
	aN[872-9]=872~=854
	aN[(56+55)-55]=true
	aN[868-84]=868+8388
	aN[(135+511)-511]=not true
	aN[864-122]=864~=858
	aN[862+37]=862+8889
	aN[860-6]=860+1267
	aN[(858-858)+863]=858+9135
	aN[(856-856)+632]=856+4325
	aN[(854-854)+604]=854~=834
	aN[630] = 3238
	aN[(869+55)-55]=850+8972
	aN[681] = 10508
	aN[846-42]=846+434
	aN[844-244]=844+2448
	aN[(842-842)+733]=842+2587
	aN[893] = 1355
	aN[838-105]=838~=880
	aN[684] = 9963
	aK = function(...)
	aN[28] = getfenv
	aN[213] = string
	aN[196] = string.char
	jY = true
	aN[105] = "format"
	aN[90] = string[aN[105]]
	local dN
	dN = nil
	cg[1] = {813493, 2363849, 91, 209, 183}
	cj[1] = nil
	dN = nil
	cf = aW[1]
	aW[1] = nil
	dN = {79, 251, 6, 169, 61, 135}
	aN[521][3][1] = ci[1]
	ci[1] = {79, 251, 6, 169, 61, 135}
	jY = true
	cg[1] = 7766777
	aY[1] = 1
	cj[1] = ""
	aN[521][3][1] = {36, 134, 100, 62, 146, 55, 106, 134, 215, 52}
	ch = {3847741, 2836119, 31, 79, 115}
	local dN
	aN[521][4][1] = ""
	aN[521][1][1] = 15847909
	dN = 1
	ck[1] = cf
	cf = nil
	aW[1] = 1
	jY = true
	aN[521][4][1] = "JSONDecode"
	eI = "JSONDecode"
	local dN
	dN = nil
	cf = {3847741, 2836119, 31, 79, 115}
	ch = nil
	dN = 7766777
	cg[1] = {36, 134, 100, 62, 146, 55, 106, 134, 215, 52}
	aN[521][3][1] = 1
	aW[1] = 7766777
	jY = true
	ch = fI[1]
	ci[1] = "JSONDecode"
	aV[1] = "JSONDecode"
	aN[521][1][1] = ch[aV[1]]
	ck[1] = cC[1]
	return aN[521][1][1](ch,ck[1])
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @2068
	aL = aK
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @3886
	)(iW,iX,iY,iZ,je,jf,jg,jh,ji,jj,jk,jl,jm,jn,jo,jp,jq,jr,js,jt,jw,jx,jy,jz,jA,jB,jC,jD,jG,jH,jI,jJ,hp,jK,jL,jM,jN,jO,jP,jQ,jW,...)end end)(ci,fu,fs,aV,ch,fv,fw,fx,ct,ck,fy,fz,fA,aN[395][24],fB,aN[395][1],fC,fP,aU,aN[395][11],fQ,fR,fS,fT,dL,aN[395][17],fU,fV,fW,fX,fY,fZ,fO,cs,ga,gb,gc,gd,aN[395][2],ge,gf)
	co[1],aN[395][7][1]=aN[395][10][1](cC)
	ft = 1
	aN[395][10][1] = ft
	fD = 2998920
	fD = 2980053
	do local dN;dE[1]=aY[1];cl=cp[1];dN=cr[1];cr[1]=cf;cf=dN;end
	fE = true
	fF = 4730253
	fG = 3004780
	fJ = 3449692
	until aN[111]
	if not co[1] then
	fD = 2983322
	do local dN;cp[1]=dC[1];cn[1]=aN[395][25][1];dN=aN[395][27][1];aN[395][27][1]=cl;cl=dN;dN=cf;cf=cj;cj=dN;end
	fE = true
	fF = 3094337
	fG = 3014119
	fJ = 3449692
	else
	fD = 2975118
	cj,cf=cf,cj
	fE = true
	fF = 4730253
	fG = 3037021
	fJ = 3449692
	end
	fE = true
	aN[395][21][1] = nil
	aN[395][21][1] = false
	local dN
	dN = {249, 11, 148, 179, 186, 215, 172}
	dG = "table"
	aN[395][25][1] = {249, 11, 148, 179, 186, 215, 172}
	dN = 500
	aY[1] = 1
	aX[1] = 500
	fE = true
	aN[395][25][1] = 30
	cn[1] = {}
	cn[1] = 30
	aN[395][21][1] = 30
	fE = true
	aN[395][4][1] = nil
	aN[395][4][1] = nil
	aN[395][16][1] = true
	local dN
	cu[1] = 30
	cr[1] = "table"
	aN[395][25][1] = cj
	cp[1] = cf
	cf = 1
	fr[1] = aW
	aW = co[1]
	co[1] = cl
	cl = dC[1]
	dC[1] = cm[1]
	dN = "table"
	dG = cC
	cC = "table"
	dN = {3285885, 1633817, 229, 127, 113}
	aX[1] = 30
	cn[1] = false
	aN[395][27][1] = {3285885, 1633817, 229, 127, 113}
	fE = true
	fE = true
	local dN
	cf = ft
	cr[1] = {3285885, 1633817, 229, 127, 113}
	dC[1] = cm[1]
	cu[1] = aN[395][25][1]
	dN = "table"
	aX[1] = 7568054
	cn[1] = "table"
	fE = true
	aN[395][13][1] = fB[1]
	aN[395][20][1] = nil
	return aN[395][13][1](aN[395][20][1],aN[395][17][1],aN[395][11][1],ct[1],aV[1],dL[1],aN[395][24][1])
	repeat fD=(5006+fD);do local dN;cg[1]=aW;dN=aY[1];aY[1]=ft;ft=dN;end;fE=true;fF=(fD-407)+(1677837+407);fG=fD+48421;fJ=fF;until aN[111]
	local dN
	aN[395][27][1] = cj
	cr[1] = cp[1]
	aW = false
	dG = cu[1]
	cu[1] = 1
	cp[1] = cg[1]
	cg[1] = 1
	dE[1] = "table"
	cn[1] = 5
	dJ[1] = 7568054
	aX[1] = cA
	cA = ft
	aN[395][26][1] = 500
	aN[395][28][1] = cC
	cC = dC[1]
	dC[1] = fr[1]
	fr[1] = aN[395][25][1]
	aN[395][25][1] = 500
	cl = co[1]
	co[1] = 7568054
	cx = cq
	cq = 1
	fE = true
	aN[395][12][1] = 404
	ft = aN[395][12][1]~=aN[395][2][1]
	aN[395][14][1] = (if ft then aN[209]~=291982 else not aN[116])
	fr[1] = aN[395][14][1]
	aN[395][16][1] = nil
	aN[395][16][1] = (if not aN[116]then not aN[395][14][1]else aN[442])
	cA = 405
	aN[395][22][1] = cA==aN[395][2][1]
	fr[1] = aN[395][22][1]
	local dN
	cm[1] = cj
	dN = "table"
	dE[1] = 7568054
	co[1] = "table"
	dN = 500
	aN[395][25][1] = dC[1]
	dC[1] = 500
	fE = true
	cr[1] = fr[1]
	aN[395][15][1] = cr[1]
	aN[395][16][1] = not fr[1]
	aN[395][6][1] = nil
	aN[395][6][1] = 400
	aX[1] = nil
	aX[1] = (if aN[209]~=291982 then aN else aN[395][2][1]==aN[395][6][1])
	cf = aX[1]
	aN[395][16][1] = not aX[1]
	co[1] = 1
	cl = {618797, 2349785, 241, 135, 221}
	cg[1] = {188}
	aN[395][28][1] = 9878848
	aN[395][8][1] = ""
	local dN
	cp[1] = false
	aW = 9878848
	aN[395][28][1] = 5
	dN = 1
	cq = ft
	ft = 1
	fE = true
	aN[395][19][1] = true
	cp[1] = true
	aN[395][13][1] = fS[1]
	local dN
	cn[1] = cq
	cu[1] = 1
	ft = true
	dN = aN[395][27][1]
	aN[395][27][1] = 500
	dC[1] = dN
	dN = dG
	dG = aX[1]
	aX[1] = dN
	fE = true
	aN[395][20][1] = eX
	aN[395][13][1][aN[395][20][1]]=ft
	ft = {}
	ft = 1
	aN[395][19][1] = (if aN[395][17][1]==ft then aN[111]else not aN[111])
	local dN
	cj = 500
	aN[395][26][1] = cC
	cC = 7568054
	dJ[1] = cx
	cx = aX[1]
	aX[1] = cr[1]
	dN = dC[1]
	dC[1] = aN[395][25][1]
	aN[395][25][1] = dN
	dN = 405
	cA = dG
	dG = 405
	fE = true
	local dN
	cC = dJ[1]
	dJ[1] = cx
	cx = aX[1]
	aX[1] = cr[1]
	cq = dC[1]
	dC[1] = 1
	cu[1] = aN[395][25][1]
	aN[395][25][1] = 500
	fE = true
	fE = true
	aN[395][5][1] = nil
	aN[395][28][1] = (if not aN[116]then aN[395][7][1]else aN[401])[(if not aN[111]then aN[401]else aN[395][5][1])]
	cp[1] = 2
	co[1] = (if not aN[111]then aN[426]else aN[395][28][1]~=cp[1])
	dC[1] = not co[1]
	ft = dC[1]
	aN[395][25][1] = ft
	local dN
	cx = 405
	dN = cg[1]
	cg[1] = cC
	cC = dN
	fE = true
	ft = {}
	ft = (if aN[111]then aN[395][25][1]else aN[403])
	cu[1] = ft
	fE = true
	if not cC then
	fD = 2975052
	aX[1],ft,cr[1],cC,cf,aY[1],cm[1],cg[1]=cg[1],cA,cC,cr[1],aN[395][27][1],ft,aY[1],aX[1]
	fE = true
	fF = 3677183
	fG = 3006604
	fJ = 3449692
	else
	fD = 2984105
	do local dN;dN=ft;ft=aY[1];aY[1]=dN;dN=cr[1];cr[1]=cC;cC=dN;end
	fE = true
	fF = 4831409
	fG = 2977225
	fJ = 3449692
	end
	aN[395][27][1] = "inflight"
	aN[395][7][1] = cs[1][aN[395][27][1]]
	aN[395][10][1] = 1
	cC = aN[395][7][1]-aN[395][10][1]
	local jZ,kg,kh=cs[1],aN[395][27][1],cC
	jZ[kg]=kh
	aN[395][16][1] = true
	local dN
	cj = cn[1]
	fr[1] = dC[1]
	cA = ft
	dN = aN[395][26][1]
	aN[395][26][1] = aY[1]
	aY[1] = cf
	cf = dN
	dN = dE[1]
	dE[1] = 405
	dG = dN
	dN = cp[1]
	cp[1] = co[1]
	co[1] = "inflight"
	aN[395][27][1] = cg[1]
	cg[1] = dJ[1]
	dJ[1] = dN
	fE = true
	aN[395][27][1] = (if aN[209]~=291982 then aN[420]else getfenv[fg])
	aN[395][7][1] = "clock"
	local ki,kj=aN[395][27][1],aN[395][7][1]
	aN[395][10][1] = ki[kj]
	cs[1] = aN[395][10][1]()
	local dN
	cj = cn[1]
	cA = ft
	dN = aN[395][27][1]
	aN[395][27][1] = "inflight"
	co[1] = dN
	dN = cg[1]
	cg[1] = dJ[1]
	dJ[1] = dN
	dN = cf
	cf = aY[1]
	aY[1] = dN
	fE = true
	cC = {}
	cC = (if aN[209]~=291982 then aN[405]else fS[1])
	cr[1] = nil
	cr[1] = "last"
	local iq,kn,im=cC,cr[1],cs[1]
	iq[kn]=im
	fE = true
	cx = co[1]~=aN[395][2][1]
	aN[395][7][1] = (if cx then not aN[111]else aN[209]==291982)
	aN[395][10][1] = aN[395][7][1]
	aN[395][8][1] = bZ(cg[1],cl,aW)
	ff = aN[395][8][1]
	fE = true
	cC = nil
	ft = nil
	aN[395][19][1] = eX
	return ft, aN[395][19][1]
	fE = true
	aN[395][10][1] = aN[395][7][1]
	cs[1] = aN[395][10][1]
	fE = true
	aN[395][8][1] = cb(cg[1],aX[1],aN[395][28][1])
	eT = aN[395][8][1]
	fE = true
	dE[1] = 1
	aN[395][28][1] = 7032852
	cg[1] = {194}
	aN[395][8][1] = ""
	aY[1] = {2675657, 3109663, 165, 131, 179}
	local dN
	cC = aN[395][27][1]
	dN = cA
	cA = ft
	ft = dN
	fE = true
	aN[395][8][1] = "a"
	bv = "a"
	local dN
	dN = aN[395][25][1]
	aN[395][25][1] = cn[1]
	cn[1] = dN
	dN = ft
	ft = 2
	cl = dN
	fE = true
	aY[1] = {1812189, 1988369, 189, 191, 25}
	dE[1] = 1
	aN[395][8][1] = ""
	cg[1] = {192, 157, 7, 24, 84, 49, 96}
	aN[395][28][1] = 1990816
	fE = true
	if not aN[395][14][1] then
	fD = 2983033
	do local dN;dC[1]=co[1];cA=cq;cq=cj;dN=aX[1];aX[1]=cl;cl=dN;end
	fE = true
	fF = 4073263
	fG = 3008640
	fJ = 3449692
	else
	fD = 2982093
	cq,cj=cj,cq
	fE = true
	fF = 4073263
	fG = 2974803
	fJ = 3449692
	end
	local dN
	cA = cj
	dE[1] = 2
	dC[1] = co[1]
	dN = cx
	cx = "inflight"
	cf = dN
	dN = cl
	cl = aX[1]
	aX[1] = dN
	fE = true
	fE = true
	cu[1] = nil
	cu[1] = (if aN[209]~=291982 then aN[457]else fB[1])
	cg[1] = nil
	return cu[1](cg[1],aN[395][17][1],aN[395][11][1],ct[1],aV[1],dL[1],aN[395][24][1])
	local dN
	cg[1] = cA
	dN = aX[1]
	aX[1] = cp[1]
	cp[1] = dN
	dN = cl
	cl = cm[1]
	cm[1] = dN
	fE = true
	aN[395][8][1] = cc(ft,cx,aN[395][28][1])
	iG = aN[395][8][1]
	fE = true
	cx = {262161, 1054369, 191, 33, 79}
	aN[395][8][1] = ""
	aW = 1
	aY[1] = {249, 88, 205, 44, 164, 50, 16, 92, 173}
	aN[395][28][1] = 152096
	local dN
	ft = cq
	dN = cn[1]
	cn[1] = cm[1]
	cm[1] = dN
	fE = true
	aN[395][8][1] = "reconnect"
	fh = "reconnect"
	fE = true
	aN[932] = 292271
	if bV==nil then
	aN[395][28][1] = 5744480
	aN[395][8][1] = ""
	cj = {2082453, 3775569, 87, 127, 181}
	aY[1] = {253, 217, 65, 84}
	aW = 1
	end
	local dN
	dN = {262161, 1054369, 191, 33, 79}
	cj = fr[1]
	fr[1] = {262161, 1054369, 191, 33, 79}
	dN = aN[395][27][1]
	aN[395][27][1] = 1
	aW = dN
	fE = true
	fE = true
	dJ[1] = 202
	cC = 202
	aY[1] = aN[395][2][1]~=cC
	aN[395][19][1] = not aY[1]
	cm[1] = aN[395][19][1]
	aN[395][13][1] = cm[1]
	aN[395][16][1] = not aN[395][19][1]
	dJ[1] = nil
	aN[395][20][1] = nil
	aN[395][12][1] = true
	cm[1] = nil
	cm[1] = true
	aN[395][13][1] = true
	fE = true
	repeat if aN[395][13][1]then fD=(2457+fD);do local dN;dN=co[1];co[1]=cm[1];cm[1]=dN;end;fE=true;fF=(fD-414)+(1100942+414);fG=69600+fD;fJ=fF;else fD=(fD+6301);cm[1],aN[395][26][1],aN[395][25][1],aY[1],co[1],dG,cr[1]=co[1],cA,aY[1],cm[1],dG,aN[395][25][1],cn[1];fE=true;fF=(fD-762)+(1283865+762);fG=(fD-252)+(71355+252);fJ=fF;end;until aN[111]
	while aN[116]do aN[945]=aN[209];end
	aN[395][19][1] = true
	cp[1] = true
	aN[395][13][1] = fS[1]
	aN[395][20][1] = "answered"
	(if aN[209]==291982 then aN[395][13][1]else aN[399])[(if aN[209]==291982 then aN[395][20][1]else aN)]=cp[1]
	aN[395][19][1] = getfenv[fg]
	aN[395][13][1] = "clock"
	aN[395][20][1] = aN[395][19][1][(if not aN[116]then aN[395][13][1]else aN[417])]
	cp[1] = aN[395][20][1]()
	fE = true
	aN[395][8][1] = ce(aN[395][26][1],cf,cr[1])
	bx = aN[395][8][1]
	local dN
	aN[395][25][1] = co[1]
	cu[1] = cr[1]
	ft = 1990816
	aN[395][27][1] = 1990816
	dE[1] = aW
	dN = 202
	cC = true
	cm[1] = 202
	fE = true
	aN[395][18][1] = (if aN[116]then aN else fS[1])
	aN[395][23][1] = {}
	aN[395][23][1] = (if aN[209]~=291982 then aN[420]else eX)
	cC = aN[395][18][1][aN[395][23][1]]
	aN[395][16][1] = not cC
	if not aN[395][16][1] then
	fD = 2975837
	aW,cj,cg[1],cq=cC,cg[1],cj,aN[395][27][1]
	fE = true
	fF = 3801984
	fG = 2998221
	fJ = 3449692
	else
	fD = 2975528
	do local dN;aW=cC;cq=aN[395][27][1];dN=aN[395][28][1];aN[395][28][1]=aY[1];aY[1]=dN;dN=cj;cj=cg[1];cg[1]=dN;end
	fE = true
	fF = 3801984
	fG = 3037209
	fJ = 3449692
	end
	local dN
	aN[395][27][1] = aY[1]
	aY[1] = "inflight"
	dN = 1990816
	ft = 2
	cg[1] = 1990816
	dN = cp[1]
	cp[1] = cj
	cj = dN
	fE = true
	local dN
	cr[1] = 152096
	cC = "inflight"
	co[1] = 405
	cl = nil
	aN[395][27][1] = "inflight"
	dN = cj
	cj = cp[1]
	cp[1] = dN
	dN = cA
	cA = dE[1]
	dE[1] = cn[1]
	cn[1] = dN
	dN = 1990816
	cg[1] = 2
	ft = 1990816
	dN = aN[395][25][1]
	aN[395][25][1] = cu[1]
	cu[1] = dN
	fE = true
	while aN[116]do aN[905]=aN[209];end
	aN[395][18][1] = fB[1]
	aN[395][23][1] = "reconnect"
	aW = 0
	return aN[395][18][1](aN[395][23][1],aN[395][17][1],aW,ct[1],aV[1],dL[1],aN[395][24][1])
	aY[1] = true
	aN[395][13][1] = true
	local dN
	cA = "inflight"
	aN[395][27][1] = cj
	fE = true
	fE = true
	ft = cp[1]
	aN[395][20][1] = nil
	aN[395][20][1] = (if aN[209]==291982 then ft else aN[403])
	cx = bx
	aN[395][12][1] = cx
	aN[395][14][1] = aN[395][7][1][aN[395][12][1]]
	dG = (if aN[395][14][1]==ct[1]then aN[209]==291982 else not aN[111])
	aN[395][20][1] = (if not aN[116]then dG else aN[412])
	local dN
	dN = 405
	co[1] = cx
	cx = 0
	aW = 405
	dN = aX[1]
	aX[1] = aN[395][27][1]
	aN[395][27][1] = dN
	fE = true
	cj = aN[395][20][1]
	if not aN[395][20][1] then
	fD = 2976364
	do local dN;dE[1]=dG;dC[1]=dJ[1];dN=cm[1];cm[1]=aN[395][25][1];aN[395][25][1]=dN;dN=cg[1];cg[1]=cj;cj=dN;end
	fE = true
	fF = 3180831
	fG = 3009152
	fJ = 3449692
	else
	fD = 2979007
	do local dN;dE[1]=dG;dN=cm[1];cm[1]=aN[395][25][1];aN[395][25][1]=dN;end
	fE = true
	fF = 3825914
	fG = 3064597
	fJ = 3449692
	end
	fE = true
	repeat if iH==nil then aN[395][8][1]=ce(cg[1],cu[1],aN[395][26][1]);iH=aN[395][8][1];end;fD=fD+3726;fD=fD+8659;do local dN;dJ[1]=cC;dN=aX[1];aX[1]=cn[1];cn[1]=dN;end;fE=true;fF,fG=(fD-954)+(964099+954),(fD-576)+(49990+576);fJ=fF;until aN[111]
	aN[395][26][1] = 14955306
	aN[395][8][1] = ""
	dE[1] = 1
	cu[1] = {2097425, 1458709, 17, 231, 41}
	cg[1] = {89}
	fE = true
	aN[395][8][1] = "}"
	iL = "}"
	local dN
	dG = aX[1]
	dN = "inflight"
	cA = dC[1]
	dC[1] = "inflight"
	dN = 2
	cj = 152096
	cr[1] = 2
	dN = cp[1]
	cp[1] = 1990816
	cq = dN
	fE = true
	aN[395][26][1] = 3832444
	dE[1] = 1
	cu[1] = {468909, 164045, 143, 57, 19}
	cg[1] = {139, 159, 73, 149}
	aN[395][8][1] = ""
	local dN
	aN[395][27][1] = cq
	dN = fr[1]
	fr[1] = true
	aN[395][28][1] = dN
	dN = 3832444
	aN[395][26][1] = 202
	cl = 3832444
	fE = true
	aN[395][8][1] = "acks"
	eP = "acks"
	local dN
	dN = 2
	cr[1] = {262161, 1054369, 191, 33, 79}
	cf = 2
	fE = true
	aN[395][28][1] = nil
	aN[395][22][1] = nil
	aN[395][15][1] = nil
	return aN[395][22][1], "clock"
	local dN
	dN = co[1]
	co[1] = "inflight"
	dC[1] = dN
	dN = dG
	dG = 1990816
	cp[1] = dN
	dN = {468909, 164045, 143, 57, 19}
	cu[1] = {262161, 1054369, 191, 33, 79}
	cr[1] = {468909, 164045, 143, 57, 19}
	fE = true
	aN[395][6][1] = fB[1]
	dJ[1] = "timeout"
	return aN[395][6][1](dJ[1],aN[395][17][1],aN[395][11][1],ct[1],aV[1],dL[1],aN[395][24][1])
	aN[395][13][1] = nil
	aN[395][13][1] = nil
	aN[395][20][1] = (if aN[209]==291982 then cs[1]else aN[432])[(if not aN[111]then aN[441]else aN[395][13][1])]
	aN[395][12][1] = "a"
	aN[395][14][1] = (if not aN[111]then aN[458]else aN[395][20][1])[(if aN[111]then aN[395][12][1]else aN[415])]
	aN[395][27][1] = aN[395][14][1]
	aN[395][19][1] = aN[395][27][1]
	local dN
	dN = cp[1]
	cp[1] = nil
	cx = dN
	fE = true
	while aN[116]do aN[928]=aN[209];end
	aN[395][28][1] = true
	aN[395][14][1] = true
	aN[395][12][1] = true
	cm[1] = fS[1]
	aW = nil
	aW = (if aN[209]==291982 then eX else aN[401])
	local kq,kr,gT=cm[1],aW,aN[395][12][1]
	kq[kr]=gT
	fE = true
	aN[395][12][1] = 1
	aN[395][14][1] = aN[395][12][1]==aN[395][17][1]
	aN[395][12][1] = nil
	aN[395][14][1] = "http"
	return aN[395][12][1], "http"
	fE = true
	cf = {468909, 164045, 143, 57, 19}
	local dN
	dG = cx
	aW = "inflight"
	dN = cm[1]
	cm[1] = 152096
	cj = dN
	fE = true
	co[1] = 1
	cg[1] = {93, 107, 104, 105, 196}
	aW = 3229903
	cl = {2073325, 1643977, 171, 219, 73}
	aN[395][8][1] = ""
	fE = true
	aN[395][8][1] = ",\"d\":"
	iF = ",\"d\":"
	fE = true
	while aN[116]do aN[1015]=aN[209];end
	cg[1] = {44}
	aW = 2351992
	aN[395][8][1] = ""
	dE[1] = 1
	cx = {1678869, 3662927, 111, 217, 217}
	local dN
	dN = cu[1]
	cu[1] = aX[1]
	aX[1] = dN
	fE = true
	aN[395][8][1] = "e"
	bB = "e"
	local dN
	dN = true
	aN[395][28][1] = 2351992
	aW = true
	fE = true
	if bz==nil then
	cg[1] = {217}
	aN[395][28][1] = 9762971
	aN[395][8][1] = ""
	dE[1] = 1
	cx = {2854257, 2169051, 87, 113, 155}
	end
	fE = true
	aN[395][8][1] = cc(cj,cl,aN[395][28][1])
	eV = aN[395][8][1]
	fE = true
	cj = {57, 142, 145, 235, 13, 211}
	cl = {1626705, 1702811, 115, 219, 19}
	aN[395][28][1] = 9274641
	aN[395][8][1] = ""
	co[1] = 1
	fE = true
	aN[395][8][1] = "random"
	iI = "random"
	fE = true
	cp[1] = aN[395][19][1]
	ck[1] = cp[1]
	fE = true
	cp[1] = 401
	aN[395][25][1] = aN[395][2][1]~=cp[1]
	aN[395][19][1] = (if aN[395][25][1]then aN[116]else not aN[116])
	aY[1] = nil
	aY[1] = (if not aN[116]then aN[395][19][1]else aN[409])
	aN[395][13][1] = aY[1]
	aN[395][16][1] = not aN[395][19][1]
	if aN[395][16][1] then
	fD = 2982776
	aN[395][28][1],cA,cq,cr[1],co[1],aN[395][27][1],dC[1],cC,cf=cf,aN[395][27][1],cu[1],aN[395][28][1],dC[1],cj,co[1],cr[1],cC
	fE = true
	fF = 3838436
	fG = 3045113
	fJ = 3449692
	else
	fD = 2983652
	do local dN;dN=cr[1];cr[1]=cf;cf=cC;cC=dN;end
	fE = true
	fF = 4258306
	fG = 2975585
	fJ = 3449692
	end
	aN[395][20][1] = "1003"
	aN[395][25][1] = aN[395][20][1]~=ch[1]
	aN[395][12][1] = not aN[395][25][1]
	fE = true
	fE = true
	cm[1] = fB[1]
	cC = "reconnect"
	return cm[1](cC,aN[395][17][1],aN[395][11][1],ct[1],aV[1],dL[1],aN[395][24][1])
	local dN
	cr[1] = 152096
	cx = 152096
	cg[1] = fr[1]
	fr[1] = {468909, 164045, 143, 57, 19}
	cu[1] = {44}
	cf = aW
	aW = co[1]
	co[1] = 9274641
	dJ[1] = 401
	cp[1] = dC[1]
	dC[1] = cm[1]
	dE[1] = 1
	cA = aN[395][27][1]
	aN[395][27][1] = dG
	dG = 202
	cn[1] = aX[1]
	aN[395][26][1] = {1678869, 3662927, 111, 217, 217}
	cq = cl
	cl = 1
	aX[1] = "reconnect"
	cC = aN[395][25][1]
	aN[395][25][1] = {468909, 164045, 143, 57, 19}
	fE = true
	aN[395][22][1] = (if not aN[111]then aN[423]else getfenv[fg])
	aN[395][15][1] = "clock"
	local ks,hP=aN[395][22][1],aN[395][15][1]
	aN[395][6][1] = ks[hP]
	cp[1] = aN[395][6][1]()
	aW = cp[1]-fs[1]
	aN[395][5][1] = fS[1]
	cA = "answered"
	dG = aN[395][5][1][cA]
	dE[1] = dG
	aN[395][16][1] = (if dG then aN[116]else aN[111])
	aN[395][3][1] = nil
	aN[395][3][1] = 300
	cn[1] = 300
	aN[395][27][1] = 300
	fE = true
	dE[1] = "b"
	fr[1] = "b"
	aN[395][19][1] = aN[395][7][1][(if not aN[111]then aN else fr[1])]
	cj = (if aN[395][11][1]~=aN[395][19][1]then aN[111]else not aN[111])
	aN[395][13][1] = nil
	aN[395][13][1] = (if aN[209]==291982 then not cj else aN[452])
	cp[1] = {}
	cp[1] = (if aN[209]~=291982 then aN[450]else aN[395][13][1])
	local dN
	dN = "answered"
	cA = 152096
	cg[1] = cj
	cj = "answered"
	fE = true
	aN[395][2][1] = "a"
	ch[1] = 0
	(if aN[209]==291982 then aU[1]else aN[456])[(if aN[111]then aN[395][2][1]else aN[451])]=ch[1]
	aN[395][2][1] = "b"
	aU[1][aN[395][2][1]]=(if aN[209]~=291982 then aN[442]else aN[395][11][1])
	aN[395][2][1] = bx
	local iA,kv,ky=aU[1],aN[395][2][1],ct[1]
	iA[kv]=ky
	aN[395][2][1] = bz
	aU[1][aN[395][2][1]]=(if not aN[111]then aN[422]else aN[395][17][1])
	aN[395][2][1] = "e"
	(if aN[116]then aN[434]else aU[1])[(if aN[116]then aN[430]else aN[395][2][1])]=aV[1]
	aN[395][1][1] = ci[1](ck[1],aU[1])
	ci[1] = 1
	aU[1] = getfenv[fg]
	aN[395][2][1] = "clock"
	ch[1] = (if not aN[116]then aU[1]else aN[404])[(if aN[116]then aN else aN[395][2][1])]
	local dN
	dN = {468909, 164045, 143, 57, 19}
	aN[395][25][1] = cp[1]
	cp[1] = {468909, 164045, 143, 57, 19}
	dN = "reconnect"
	aW = 152096
	cr[1] = "reconnect"
	fE = true
	ci[1] = fS[1]
	cp[1] = nil
	cp[1] = "terminal"
	aU[1] = "terminal"
	aN[395][2][1] = ci[1][aU[1]]
	ch[1] = (if aN[395][2][1]then aN[116]else aN[209]==291982)
	aN[395][16][1] = not ch[1]
	aU[1] = gf[1]
	ci[1] = aU[1]()
	aN[395][2][1] = fP[1]
	ch[1] = nil
	ch[1] = "JSONEncode"
	cs[1] = (if not aN[111]then aN else aN[395][2][1])[(if not aN[116]then ch[1]else aN[422])]
	aN[395][27][1] = {}
	aN[395][7][1] = "a"
	aN[395][10][1] = fR[1]
	co[1] = ""
	cr[1] = aN[395][10][1]..co[1]
	(if aN[209]==291982 then aN[395][27][1]else aN[441])[(if not aN[116]then aN[395][7][1]else aN)]=cr[1]
	aN[395][7][1] = "b"
	fE = true
	aN[395][10][1] = fZ[1]
	aN[395][27][1][aN[395][7][1]]=(if aN[209]==291982 then aN[395][10][1]else aN[411])
	fr[1] = bx
	aN[395][7][1] = (if aN[111]then fr[1]else aN)
	aN[395][27][1][aN[395][7][1]]=(if aN[116]then aN[424]else ci[1])
	aU[1] = cs[1](aN[395][2][1],aN[395][27][1])
	aN[395][2][1] = fS[1]
	ch[1] = nil
	ch[1] = "inflight"
	cs[1] = aN[395][2][1][ch[1]]
	fr[1] = 1
	aN[395][27][1] = 1
	aN[395][7][1] = cs[1]+aN[395][27][1]
	aN[395][2][1][ch[1]]=aN[395][7][1]
	cs[1] = {}
	cs[1] = (if aN[111]then fX[1]else aN)
	aN[395][27][1] = "https://api.polsec.net/runtime/socket/http"
	local dN
	aN[395][28][1] = 152096
	ft = aN[395][25][1]
	dC[1] = 152096
	aN[395][25][1] = {44}
	fE = true
	aN[395][7][1] = fl
	aN[395][10][1] = aU[1][aN[395][7][1]]
	cC = {}
	cC = 1
	cr[1] = 2
	aX[1] = -2
	aN[395][28][1] = aN[395][10][1](aU[1],cC,aX[1])
	fr[1] = nil
	fr[1] = ",\"d\":"
	co[1] = {}
	co[1] = ",\"d\":"
	cn[1] = "}"
	aN[395][19][1] = aN[395][1][1]..cn[1]
	aN[395][13][1] = co[1]..aN[395][19][1]
	aN[395][20][1] = aN[395][28][1]..aN[395][13][1]
	aN[395][2][1],ch[1]=cs[1](aN[395][27][1],aN[395][20][1],dL[1])
	cs[1] = fS[1]
	local dN
	cu[1] = ",\"d\":"
	dN = "answered"
	dJ[1] = 401
	cl = "answered"
	dN = cq
	cq = {44}
	dG = dN
	fE = true
	fE = true
	local dN
	dG = 152096
	cA = 1
	aY[1] = "b"
	dN = 152096
	dC[1] = cf
	cf = 152096
	dN = {44}
	aN[395][25][1] = 1
	cC = {44}
	fE = true
	aN[395][16][1] = (if cs[1]then aN[116]else aN[209]==291982)
	if aN[395][16][1] then
	fD = 2976865
	ft,aN[395][27][1],cn[1],dC[1],aX[1],fr[1],aN[395][26][1],dG,cC,cl,cf,dJ[1],cj,cx,cp[1],cm[1],aY[1],cu[1],cr[1],co[1],cg[1],dE[1]=aY[1],aX[1],dJ[1],ft,aN[395][26][1],cC,cp[1],aN[395][25][1],cx,cq,cu[1],cj,co[1],cf,dG,cA,cl,dC[1],cg[1],cn[1],fr[1],aW
	fE = true
	fF = 3215095
	fG = 3050108
	fJ = 3449692
	else
	fD = 2984165
	cn[1],cl,cu[1],cf,cp[1]=cp[1],cu[1],cf,cl,cn[1]
	fE = true
	fF = 3677183
	fG = 3014177
	fJ = 3449692
	end
	aY[1] = {}
	aY[1] = true
	aN[395][10][1] = true
	aN[395][25][1] = fS[1]
	dG = "answered"
	aN[395][25][1][dG]=(if aN[209]~=291982 then aN[403]else aN[395][10][1])
	aN[395][10][1] = #ch[1]
	aY[1] = {}
	aY[1] = 65536
	aN[395][25][1] = (if aY[1]<=aN[395][10][1]then aN[209]==291982 else aN[116])
	aY[1] = true
	aN[395][10][1] = true
	aN[395][25][1] = fS[1]
	dG = (if not aN[116]then eT else aN[420])
	local kz,kC,kD=aN[395][25][1],dG,aN[395][10][1]
	kz[kC]=kD
	fE = true
	aN[1045] = 292515
	dE[1] = 1
	cl = 15847909
	aN[395][8][1] = ""
	cu[1] = {2673189, 777891, 179, 165, 11}
	cg[1] = {230, 223, 58, 127, 4, 182, 111, 152}
	local dN
	co[1] = "answered"
	dN = "terminal"
	cp[1] = {44}
	aN[395][26][1] = "terminal"
	fE = true
	aN[395][8][1] = "rejected"
	iJ = "rejected"
	fE = true
	if bb==nil then
	aN[395][8][1] = ""
	fr[1] = {}
	cl = 506381
	cu[1] = {3649009, 1959353, 231, 233, 217}
	dE[1] = 1
	end
	local dN
	aN[395][27][1] = "answered"
	co[1] = 1
	aX[1] = 15847909
	fE = true
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @81750
	aM = aK
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @83824
	return hp(aN[534][11],fu,fv,cs,aN[534][14],aN[534][6],aW,aN[534][5],fw,aN[534][4],aN[534][2],aX,dJ,aY,fx,aN[534][18],ck,aN[534][17],aN[534][12],cu,dC,aN[534][9],cm,co,cC,cx,dE,...)end
	cs[1] = nil
	dL[1] = (if aX[1]then aN[223]else aN[30])
	fD = 273107
	aN[534][16][1] = nil
	aN[534][16][1] = nil
	aN[534][21][1] = true
	fD = 274234
	if aN[534][21][1]then fD=(fD+1034);cn,cf,ct[1],ch[1]=cf,ch[1],aN[534][23][1],cn;fE=true;fF,fG=(fD-488)+(1293068+488),fD+31111;fJ=fF;else fD=(fD+5381);aN[534][22][1],cn,cA,cf,cr[1],ct[1],ch[1]=cr[1],cA,cf,ch[1],aN[534][22][1],aN[534][23][1],cn;fE=true;fF,fG=fD+1293068,(fD-946)+(62868+946);fJ=fF;end
	end end else
	-- sub-region (fF,fG) base fD:
	local dN
	dN = nil
	aN[534][23][1] = nil
	ft[1] = nil
	fE = true
	aN[986] = 632597
	local dN
	fr[1] = 1
	dN = nil
	cp[1] = nil
	aN[534][20][1] = nil
	dN = nil
	ft[1] = nil
	ch[1] = nil
	fE = true
	local dN
	cp[1] = "Wait"
	cg = nil
	cf = nil
	aU[1] = nil
	cn = nil
	dN = nil
	aN[534][20][1] = nil
	ct[1] = nil
	fE = true
	local dN
	aV = nil
	cp[1] = nil
	aU[1] = nil
	ch[1] = nil
	dN = nil
	ct[1] = nil
	aN[534][20][1] = nil
	dN = nil
	aN[534][21][1] = nil
	cn = nil
	cg = nil
	fE = true
	aN[534][3][1] = true
	ct[1] = true
	ch[1] = true
	local dN
	aV = nil
	dN = nil
	aN[534][20][1] = true
	ct[1] = nil
	dN = true
	ch[1] = nil
	aU[1] = true
	dN = nil
	cg = nil
	aN[534][21][1] = nil
	fE = true
	if not((fG-fD)<=60446 or(fG-fD)>=60781)then if bw==nil then aN[534][7][1]=1;cn={(207+21)-21};aV='';aN[534][1][1]=((fD+6003871)-(fD+331545));aN[534][8][1]={((fD+1744948)-(fD+818047)),((fD+2430178)-(fD+153439)),((fD+347339)-(fD+347234)),((fD+469196)-(fD+469173)),((fD+513826)-(fD+513725))};end;fD=(fD+2833);fD=7546+fD;ft[1],fr[1],aN[534][21][1],aU[1],ch[1]=aU[1],aN[534][21][1],ch[1],ft[1],fr[1];fE=true;fF=(fD-401)+(347017+401);fG=fD+819;fJ=fF;elseif 819==(fG-fD)then if bw==nil then aV=cb(cn,aN[534][8][1],aN[534][1][1]);bw=aV;end;fD=7892+fD;fD=(fD+9268);do local dN;dN=cn;cn=aN[534][21][1];aN[534][21][1]=dN;dN=ft[1];ft[1]=cf;cf=dN;end;fE=true;fF=347017+fD;fG=(fD-138)+(74958+138);fJ=fF;elseif 74958==(fG-fD)then if fa==nil then aN[534][7][1]=1;aN[534][1][1]=((fD+7832026)-(fD+958509));aV='';aN[534][8][1]={((fD+1001759)-(fD+305094)),((fD+680705)-(fD+355784)),((fD+117170)-(fD+117159)),((fD+645000)-(fD+644955)),((fD+581082)-(fD+580989))};aN[534][21][1]={131,32,(172+3)-3,76,213,223,16,204};end;fD=(fD+6422);fD=fD+8891;cn,ch[1],aV,cg,cq[1]=cg,cn,cr[1],ch[1],aV;fE=true;fF=347017+fD;fG=(fD-432)+(1433+432);fJ=fF;elseif not(1433~=(fG-fD))then if fa==nil then cq[1]=bZ(aN[534][21][1],aN[534][8][1],aN[534][1][1]);fa=cq[1];end;fD=(4575+fD);fD=8913+fD;do local dN;cp[1]=aN[534][20][1];dN=aV;aV=ch[1];ch[1]=cg;cg=dN;dN=cf;cf=ft[1];ft[1]=dN;end;fE=true;fF=fD+347017;fG=53241+fD;fJ=fF;elseif(fG-fD)==53241 then if eY==nil then aN[534][8][1]={((fD+1233253)-(fD+227416)),((fD+2708279)-(fD+858444)),((fD+268165)-(fD+267914)),((fD+686234)-(fD+685991)),((fD+690227)-(fD+690192))};aN[534][7][1]=1;cq[1]='';aN[534][21][1]={197,182,(243-2)+2};aN[534][1][1]=((fD+17242645)-(fD+587806));end;fD=(709+fD);fD=(8865+fD);aV,cp[1]=cp[1],aV;fE=true;fF,fG=fD+1566428,(fD-877)+(81160+877);fJ=fF;end end end end end else
	if 1192460>=(fF-fD)then if not((fF-fD)>1029361)then if 1029361>(fF-fD)then if 966154>=(fF-fD)then if not((fF-fD)>845345)then if 61227==(fG-fD)then while aN[223]do aN[929]=aN[85];end;if eF==nil then aV=ce(cr[1],aN[534][8][1],aN[534][1][1]);eF=aV;end;fD=(8407+fD);fD=fD+2420;cA,fr[1]=fr[1],cA;fE=true;fF=(fD-574)+(740313+574);fG=41416+fD;fJ=fF;end else if not(27224~=(fG-fD))then fs[1]=(if aN[30]then aN[552]else aN[596]);fs[1]=(if aN[85]~=631730 then aN[536]else(67930+(-67930)));fD=(fD+9194);dG[1]=(if fs[1]<=(if not aN[30]then aN[557]else cA)then aN[85]==631730 else aN[85]~=631730);ci[1]=(if dL[1]<=aN[534][16][1]then not aN[223]else aN[223]);cl[1]=aN[534][16][1]<=dL[1];ft[1]=not dG[1];fD=fD+8145;aN[534][10][1]=dG[1]and ci[1];aN[534][20][1]=ft[1]and(if aN[85]==631730 then cl[1]else aN);fD=fD+9323;fD=2734+fD;ch[1],aN[534][21][1],cA,aU[1],cr[1]=cn,cA,cq[1],cr[1],aU[1];fE=true;fF,fG=(fD-169)+(966154+169),46304+fD;fJ=fF;elseif 46304==(fG-fD)then while aN[223]do aN[1025]=aN[85];end;ch[1]=aN[534][10][1]or(if not aN[223]then aN[534][20][1]else aN);fD=(fD+7079);if not ch[1]then fD=8753+fD;cA,cp[1],cr[1],ft[1],aN[534][20][1],cn,cg=ft[1],aN[534][20][1],cg,cA,cp[1],aU[1],cr[1];fE=true;fF=(fD-985)+(966154+985);fG=87736+fD;fJ=fF;else fD=(7212+fD);do local dN;cn=aU[1];dN=aN[534][20][1];aN[534][20][1]=cp[1];cp[1]=dN;dN=cr[1];cr[1]=cg;cg=dN;end;fE=true;fF=966154+fD;fG=fD+63173;fJ=fF;end;elseif not(63173~=(fG-fD))then fD=4266+fD;do local dN;cf=aV;aU[1]=ct[1];dN=cA;cA=ft[1];ft[1]=dN;dN=cn;cn=aN[534][21][1];aN[534][21][1]=dN;end;fE=true;fF=fD+966154;fG=13363+fD;fJ=fF;elseif not(87736~=(fG-fD))then fD=(fD+903);do local dN;aU[1]=aN[534][22][1];cf=ch[1];aN[534][23][1]=fr[1];ch[1]=cg;cg=cp[1];dN=aV;aV=cA;cA=aN[534][20][1];aN[534][20][1]=dN;dN=aN[534][21][1];aN[534][21][1]=ct[1];ct[1]=ft[1];ft[1]=cn;cn=cr[1];cr[1]=dN;end;fE=true;fF=1558248+fD;fG=(fD-370)+(91902+370);fJ=fF;elseif not(13401<=(fG-fD)or 13219>=(fG-fD))then aN[1017]=aN[85]+778;cj[1]=dL[1];cl[1]=aN[54][bK];fD=(fD+16727);cA=function(...)local kE=function(...)
	-- for-dispatch over kF=799..964 step 5
	aH = 0
	aH = 1
	aN = {}
	aH = 1014
	aN[608] = 9077
	aM = true
	aN[148] = false
	aN[834+63]=834+3701
	aN[616] = true
	aN[844-243]=844~=904
	aN[84] = 220359
	aN[(859-859)+792]=859+1732
	aN[(198+420)-420]=not false
	aN[869-113]=869+8180
	aN[728] = 9652
	aN[(611+455)-455]=879+8628
	aN[884-275]=884+999
	aN[830] = true
	aN[894-98]=894+7569
	aN[899-107]=899+3072
	aN[797] = 6151
	aN[(846+282)-282]=909+4004
	aN[(721+123)-123]=914+7394
	aN[(919-919)+621]=919+8438
	aN[924-136]=924+8726
	aN[(689+219)-219]=929~=819
	aN[(752+43)-43]=934+101
	aN[939-137]=939+7464
	aN[944-211]=944+4323
	aN[873] = 8955
	aY = function(...)
	while aN[148]do aN[1014]=aN[84];end
	aN[159] = getfenv
	aN[203] = string
	aN[177] = string.char
	local dN
	dN = aX[1]
	aX[1] = nil
	cs = co[1]
	co[1] = 1
	cq[1] = dN
	cB = true
	dC = 255164
	ck[1] = {204, 215, 227, 172}
	cm[1] = 13764085
	ct[1] = {2063433, 792497, 141, 217, 103}
	cu[1] = ""
	co[1] = 1
	local dN
	aU[1] = nil
	aX[1] = 12872556
	dN = cq[1]
	cq[1] = nil
	ch[1] = dN
	cB = true
	cC,dC=cA+747400,11555+cA
	cu[1] = "Body"
	eE = "Body"
	local dN
	aY = nil
	dN = cs
	cs = nil
	cl[1] = dN
	dN = {813493, 2363849, 91, 209, 183}
	cj[1] = nil
	aN[556][2][1] = {813493, 2363849, 91, 209, 183}
	dN = nil
	aU[1] = 12872556
	aX[1] = nil
	cB = true
	dC = 263759
	cm[1] = 6482274
	co[1] = 1
	ct[1] = {3124485, 1736455, 175, 147, 169}
	cu[1] = ""
	ck[1] = {22, 153, 126}
	cB = true
	dC = 268472
	cu[1] = "Url"
	eO = "Url"
	local dN
	dN = ch[1]
	ch[1] = nil
	ci = {813493, 2363849, 91, 209, 183}
	cp[1] = nil
	cs = dN
	cB = true
	dC = 236906
	repeat aN[57]=string.char(((175+256-73)-(((175+256-73))//256)*256),((73+256-218)-(((73+256-218))//256)*256),((149+256-35)-(((149+256-35))//256)*256),((171+256-62)-(((171+256-62))//256)*256),((38+256-197)-(((38+256-197))//256)*256),((139+256-23)-(((139+256-23))//256)*256));aN[188]=string[aN[57]];cA=(8787+cA);cA=(9181+cA);aW[1],cg,cr[1],cs,cj[1]=cj[1],cr[1],cg,aW[1],cs;cB=true;cC,dC=(cA-897)+(1610053+897),(cA-417)+(99813+417);dJ=cC;until aN[198]
	aV[1] = {1015613, 1184851, 233, 151, 233}
	ck[1] = {163, 225, 144}
	aX[1] = 1
	cm[1] = 1653017
	cq[1] = ""
	local dN
	dN = nil
	aY = nil
	cf[1] = nil
	dN = ct[1]
	ct[1] = nil
	cn = dN
	dN = 1
	co[1] = "Url"
	cu[1] = 1
	cB = true
	cC,dC=cA+1610053,24220+cA
	cq[1] = "GET"
	kI = "GET"
	local dN
	aN[556][2][1] = cs
	cs = "Url"
	aN[556][3][1] = nil
	dN = {813493, 2363849, 91, 209, 183}
	ci = "GET"
	cq[1] = {813493, 2363849, 91, 209, 183}
	dN = cl[1]
	cl[1] = 12872556
	aU[1] = dN
	cB = true
	dC = 317903
	ci = ""
	aV[1] = {3373209, 433513, 121, 103, 173}
	cm[1] = 2793863
	aX[1] = 1
	ck[1] = {240}
	local dN
	dN = "Url"
	cs = nil
	ct[1] = "Url"
	cB = true
	cC,dC=cA+195585,cA+3679
	cs = ce(cm[1],aX[1],aN[556][2][1])
	eN = cs
	local dN
	cf[1] = nil
	dN = {3373209, 433513, 121, 103, 173}
	aV[1] = "Url"
	co[1] = {3373209, 433513, 121, 103, 173}
	cB = true
	cC,dC=cA+1746988,cA+40729
	cm[1] = {23}
	aN[556][2][1] = 2710219
	cs = ""
	aX[1] = {2624545, 2610033, 99, 3, 205}
	cx[1] = 1
	cB = true
	dC = 296615
	cs = "a"
	bv = "a"
	cB = true
	dC = 306927
	aN[556][2][1] = 12864471
	cs = ""
	cx[1] = 1
	co[1] = {177, 72, 215, 155, 54, 116, 64, 237}
	aX[1] = {786177, 85343, 197, 13, 5}
	cB = true
	cC,dC=cA+1746988,92092+cA
	cn = "tonumber"
	fo = "tonumber"
	cB = true
	cC,dC=399146+cA,(cA-479)+(6750+479)
	cr[1] = fy[1]
	aW[1] = {}
	cl[1] = nil
	cl[1] = "Url"
	aN[556][4][1] = nil
	cf[1] = fA[1]
	cm[1] = nil
	cx[1] = fU[1]
	cq[1] = nil
	cu[1] = (if not aN[148]then cx[1]..cq[1]else aN[615])
	ci = cm[1]..cu[1]
	aY = cf[1]..ci
	aN[556][3][1] = aN[556][4][1]..aY
	aW[1][cl[1]]=aN[556][3][1]
	cl[1] = nil
	cl[1] = nil
	aN[556][4][1] = "GET"
	local it,kR,kS=aW[1],cl[1],aN[556][4][1]
	it[kR]=kS
	cp[1] = cr[1](aW[1])
	aW[1] = {}
	aW[1] = (if aN[84]~=220359 then aN[599]else getfenv[fo])
	cj[1] = eN
	cl[1] = cj[1]
	local dN
	ck[1] = {786177, 85343, 197, 13, 5}
	dN = nil
	aN[556][1][1] = cl[1]
	cl[1] = nil
	cB = true
	dC = 438545
	aN[556][4][1] = cp[1][(if aN[84]~=220359 then aN[615]else aN[556][1][1])]
	cf[1] = (if aN[84]~=220359 then aN else aW[1])(aN[556][4][1])
	cl[1] = cf[1]
	cm[1] = cl[1]
	aV[1] = not cf[1]
	local kV=aV[1]
	cB = true
	cC,dC=(if kV then 399146+cA else 399146+cA),(if kV then(cA-696)+(53039+696)else(cA-248)+(60029+248))
	cB = true
	cC,dC=cA+1043660,cA+49927
	cB = true
	dC = 490739
	cx[1] = 0
	cj[1] = 0
	cm[1] = 0
	cB = true
	cC,dC=1043660+cA,49927+cA
	cx[1] = {3370521, 3607675, 165, 107, 205}
	cu[1] = ""
	co[1] = 1
	ck[1] = {80}
	cm[1] = 5720013
	cB = true
	dC = 524852
	cu[1] = "/"
	kG = "/"
	local dN
	aV[1] = 5720013
	cm[1] = {80}
	cx[1] = 1
	cB = true
	dC = 496006
	cu[1] = ""
	cm[1] = {243, 154, 60, 158, 221, 102}
	ck[1] = {1832989, 400069, 139, 177, 29}
	cx[1] = 1
	aV[1] = 14458417
	local dN
	dN = cf[1]
	cf[1] = 1
	cj[1] = aW[1]
	aW[1] = dN
	cB = true
	cC,dC=cA+1822214,97239+cA
	cu[1] = "Method"
	eK = "Method"
	local dN
	dN = aN[556][4][1]
	aN[556][4][1] = {786177, 85343, 197, 13, 5}
	cq[1] = dN
	dN = {786177, 85343, 197, 13, 5}
	ct[1] = cl[1]
	cl[1] = {786177, 85343, 197, 13, 5}
	cB = true
	dC = 538132
	cu[1] = ""
	aV[1] = 15365948
	cm[1] = {26, 39, 191, 112, 55, 196, 166, 0, 55, 188, 122, 217, 148, 132, 219, 202, 60, 62, 97, 159, 106, 27, 188, 200, 89, 137, 93, 153, 161, 240, 230, 231, 221, 219, 186, 235, 69, 14}
	cx[1] = 1
	ck[1] = {1686369, 2288091, 129, 19, 147}
	local dN
	aN[556][1][1] = aY
	aY = ci
	cB = true
	dC = 536413
	cu[1] = "https://api.polsec.net/loader/session/"
	kO = "https://api.polsec.net/loader/session/"
	cB = true
	cC,dC=761831+cA,cA+55840
	while aN[148]do aN[1030]=aN[84];end
	cu[1] = ""
	cx[1] = 1
	ck[1] = {1060489, 1427357, 89, 123, 255}
	cm[1] = {148, 156, 74, 176, 118, 18, 214, 127, 198}
	aN[556][2][1] = 6558502
	local dN
	cg = cn
	co[1] = 1
	dN = aN[556][1][1]
	aN[556][1][1] = cj[1]
	cj[1] = dN
	cB = true
	cC,dC=cA+761831,(cA-215)+(8090+215)
	cu[1] = "?socket=1"
	kH = "?socket=1"
	cB = true
	cC,dC=(cA-193)+(761831+193),80966+cA
	if eN==nil then
	cx[1] = 1
	cs = ""
	cm[1] = {89, 181, 11, 100, 15, 102, 74, 224, 5, 240}
	ck[1] = {2852925, 3856229, 129, 139, 17}
	aN[556][2][1] = 11537647
	end
	local dN
	cn = aU[1]
	dN = {1060489, 1427357, 89, 123, 255}
	ck[1] = aX[1]
	aX[1] = {1060489, 1427357, 89, 123, 255}
	dN = 0
	cu[1] = cq[1]
	cq[1] = 0
	cB = true
	dC = 605867
	ci = cc(ck[1],aV[1],cm[1])
	bw = ci
	local dN
	aN[556][4][1] = aU[1]
	co[1] = {1060489, 1427357, 89, 123, 255}
	dN = cu[1]
	cu[1] = ci
	ci = dN
	cB = true
	dC = 613510
	co[1] = 1
	aV[1] = {568525, 3431757, 29, 145, 175}
	ck[1] = {132, 119, 228, 191, 40, 180, 237, 44, 123, 139}
	cu[1] = ""
	cm[1] = 1262377
	local dN
	aN[556][1][1] = "?socket=1"
	cs = aY
	dN = ct[1]
	ct[1] = {568525, 3431757, 29, 145, 175}
	aV[1] = dN
	cB = true
	dC = 659588
	while aN[148]do aN[978]=aN[84];end
	cu[1] = "JSONDecode"
	eI = "JSONDecode"
	cB = true
	cC,dC=747400+cA,(cA-670)+(59858+670)
	cr[1] = 1262377
	fr[1] = 1262377
	aW[1] = fu[1]
	aN[556][1][1] = "JSONDecode"
	local dN
	ch[1] = aN[556][4][1]
	cq[1] = {568525, 3431757, 29, 145, 175}
	ct[1] = aV[1]
	cB = true
	cC,dC=1043660+cA,cA+49183
	aN[917] = 220592
	cg = aW[1][(if not aN[148]then aN[556][1][1]else aN[574])]
	aY = "Body"
	cj[1] = "Body"
	ch[1] = "Body"
	cm[1] = ck[1][(if aN[84]==220359 then ch[1]else aN)]
	cr[1] = cg(aW[1],cm[1])
	aW[1] = {}
	aW[1] = (if aN[148]then aN[560]else getfenv[fo])
	aN[556][1][1] = nil
	aN[556][1][1] = "a"
	cg = cr[1][(if aN[84]~=220359 then aN[585]else aN[556][1][1])]
	ch[1] = (if aN[148]then aN[576]else aW[1])(cg)
	aY = bw
	local dN
	aN[556][4][1] = "a"
	dN = aU[1]
	aU[1] = 1
	co[1] = dN
	dN = aY
	aY = cr[1]
	cr[1] = dN
	dN = aW[1]
	aW[1] = cx[1]
	cx[1] = dN
	cB = true
	cC,dC=(cA-316)+(1043660+316),29568+cA
	cj[1] = cr[1]
	cm[1] = nil
	cm[1] = nil
	aW[1] = (if not aN[198]then aN[562]else aY)[(if aN[198]then cm[1]else aN[557])]
	return ch[1], aW[1]
	-- region end
	-- warn: repeat-until 'aN[198]' not pre-true; one-shot assumed
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @13254
	aQ = aY
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @15360
	return kE(aN[534][11],cj,fu,fv,cs,aN[534][14],aN[534][6],aW,aN[534][5],fw,aN[534][4],aN[534][2],aX,dJ,aY,fx,aN[534][18],ck,aN[534][17],aN[534][12],cu,dC,aN[534][9],cm,co,cC,cx,dE,...)end
	fD = 271826
	fs[1],dG[1],ci[1]=cl[1](cA)
	fD = 270159
	fD = 270568
	aN[534][20][1],cA=cA,aN[534][20][1]
	fE = true
	fF = 1631155
	fG = 310747
	fJ = 582328
	end end else
	-- sub-region (fF,fG) base fD:
	while aN[223]do aN[1020]=aN[85];end
	aN[534][20][1] = cc(cp[1],aN[534][8][1],aN[534][1][1])
	eQ = aN[534][20][1]
	fE = true
	aN[534][20][1] = ""
	aN[534][7][1] = 1
	aN[534][8][1] = {1364997, 3186867, 181, 253, 233}
	aN[534][1][1] = 15818604
	cp[1] = {119, 240, 249, 114, 184, 82, 149, 33}
	fE = true
	-- sub-region (fF,fG) base fD:
	while aN[223]do aN[983]=aN[85];end
	fE = true
	if 1129020>=(fF-fD)then if 1129020>(fF-fD)then if 1085945<=(fF-fD)then if 1085945<=(fF-fD)then if 82315==(fG-fD)then cl[1]=3;aV=(if cl[1]>cj[1]then aN[30]else aN[85]~=631730);fD=(8673+fD);cA=not aV;fD=fD+9526;fD=5109+fD;cr[1],cg,aV,cA=cA,aV,cg,cr[1];fE=true;fF=1085945+fD;fG=(fD-268)+(13142+268);fJ=fF;elseif 13142==(fG-fD)then if cr[1]then fD=(fD+9961);do local dN;aU[1]=fr[1];dN=cr[1];cr[1]=ft[1];ft[1]=aN[534][23][1];aN[534][23][1]=aN[534][21][1];aN[534][21][1]=dN;dN=cg;cg=ch[1];ch[1]=aV;aV=dN;end;fE=true;fF=449834+fD;fG=fD+22068;fJ=fF;else fD=fD+7316;do local dN;aU[1]=fr[1];dN=aV;aV=ch[1];ch[1]=dN;dN=aN[534][23][1];aN[534][23][1]=cr[1];cr[1]=ft[1];ft[1]=dN;end;fE=true;fF=fD+1085945;fG=fD+54368;fJ=fF;end;elseif 54368==(fG-fD)then cl[1]=aN[54][bR];cg=fp;aN[534][10][1]=(if aN[85]==631730 then cl[1]else aN[538])[(if not aN[223]then cg else aN[580])];aV=aN[534][10][1](cj[1]);fD=(17528+fD);fD=fD+6951;do local dN;dN=ft[1];ft[1]=cr[1];cr[1]=dN;dN=cg;cg=aV;aV=dN;end;fE=true;fF,fG=(fD-606)+(1085945+606),fD+29190;fJ=fF;elseif not((fG-fD)~=29190)then fD=334+fD;aN[534][21][1],aN[534][23][1],ft[1],cr[1]=aN[534][23][1],aN[534][21][1],cr[1],ft[1];fE=true;fF,fG=449834+fD,(fD-719)+(22068+719);fJ=fF;end end else if(fF-fD)==1053113 then if 56065>(fG-fD)and 55789<(fG-fD)then aN[534][22][1]=ci[1];fD=(8588+fD);if ci[1]then fD=(6197+fD);do local dN;cp[1]=cf;dN=ch[1];ch[1]=aN[534][23][1];aN[534][23][1]=cg;cg=aV;aV=dN;end;fE=true;fF,fG=1053113+fD,fD+11999;fJ=fF;else fD=(1129+fD);do local dN;cp[1]=cf;dN=cq[1];cq[1]=ch[1];ch[1]=aN[534][23][1];aN[534][23][1]=cg;cg=aV;aV=dN;end;fE=true;fF=fD+1053113;fG=fD+14023;fJ=fF;end;elseif not((fG-fD)<=11126 or(fG-fD)>=12671)then fD=8236+fD;do local dN;dN=cr[1];cr[1]=cn;cn=dN;dN=ct[1];ct[1]=cp[1];cp[1]=dN;dN=aU[1];aU[1]=cq[1];cq[1]=aV;aV=dN;end;fE=true;fF,fG=fD+343171,(fD-161)+(98060+161);fJ=fF;elseif 14023==(fG-fD)then repeat fD=fD+7617;cr[1],cn=cn,cr[1];fE=true;fF,fG=fD+1053113,(fD-950)+(25995+950);fJ=fF;until aN[30];elseif not((fG-fD)~=25995)then aN[534][13][1]=bI;fD=fD+698;cg=aN[534][13][1];aN[534][10][1]=cg;cg=(if not aN[223]then aN[534][10][1]else aN[536]);fD=fD+14057;aN[534][22][1]=cg;fD=(fD+2448);fD=fD+9764;aU[1],ct[1],cp[1],aV=aV,cp[1],ct[1],aU[1];fE=true;fF=fD+343171;fG=fD+98060;fJ=fF;end end end else if 1129020>=(fF-fD)then if(fG-fD)==30205 then repeat if bJ==nil then fr[1]='';aN[534][21][1]={145,130,(67-13)+13,212,157,140,127,59,227,(100-8)+8,211,225};aN[534][1][1]=((fD+5701201)-(fD+715824));aN[534][7][1]=1;aN[534][8][1]={((fD+2269074)-(fD+321165)),((fD+908284)-(fD+636277)),((fD+683619)-(fD+683570)),((fD+650083)-(fD+649954)),((fD+657229)-(fD+657208))};end;fD=(fD+4996);fD=2371+fD;do local dN;cp[1]=cq[1];dN=fr[1];fr[1]=aN[534][22][1];aN[534][22][1]=aU[1];aU[1]=dN;end;fE=true;fF,fG=(fD-896)+(495041+896),55654+fD;fJ=fF;until aN[30];end end end else if 1152002<(fF-fD)then if 1180144<(fF-fD)then if not((fF-fD)>1192460)then if(fG-fD)==96676 then aU[1]=(if aN[223]then aN[596]else dE[1]);ck[1]=aU[1];fD=(fD+1505);cm[1]=function(...)local kW=function(...)
	-- for-dispatch over hq=491..380 step -3
	aN = {}
	aH = 1059
	aN[(485-485)+852]=485+7914
	aN[(482-482)+877]=482~=443
	aM = true
	aN[(476-476)+695]=476+8004
	aN[473+216]=473+845
	aN[(753+374)-374]=470+5713
	aN[(681+202)-202]=467+1159
	aN[464-443]=464==464
	aN[461+282]=461+4081
	aN[828] = true
	aN[455+255]=455+581
	aN[(39+148)-148]=452~=452
	aN[449+293]=449+8027
	aN[(636+473)-473]=446~=476
	aN[443+451]=443+6261
	aN[(685+183)-183]=440~=419
	aN[(437-437)+807]=437+3324
	aN[(434-434)+664]=434+5491
	aN[431+189]=431+5936
	aN[428+283]=428+6951
	aN[425+314]=425+5430
	aN[(885+306)-306]=422~=380
	aN[(419-419)+665]=419~=458
	aN[416+393]=416+8707
	aN[(821+284)-284]=413+652
	aN[(410-410)+874]=410+6568
	aN[(407-407)+806]=407+7398
	aN[716] = 594
	aN[401+205]=401+9668
	aN[146] = 111236
	aN[(654+198)-198]=395+6565
	aN[392+443]=392+3495
	aN[389+346]=389+2137
	aK = function(...)
	aN[49] = getfenv
	aN[153] = string
	aN[3] = string.char
	kY = true
	cu = 317334
	local dN
	aV[1] = 1
	cq[1] = nil
	cg = aN[540][1][1]
	cj = nil
	aN[540][1][1] = "Wait"
	cs[1] = nil
	ck = nil
	dN = nil
	aU[1] = nil
	aN[540][4][1] = co[1]
	co[1] = nil
	kY = true
	ct,cu=651444+dG,(dG-61)+(76074+61)
	cl = cb(cq[1],cm[1],aW[1])
	kX = cl
	local dN
	dN = aN[540][4][1]
	aN[540][4][1] = nil
	cq[1] = dN
	dN = nil
	co[1] = cg
	cg = nil
	dN = nil
	cf = "Wait"
	aN[540][1][1] = nil
	kY = true
	cu = 364438
	co[1] = {}
	aV[1] = {}
	kY = true
	cu = 379117
	co[1] = #aV[1]
	ci[1] = 64
	cp[1] = 64
	cs[1] = (if aN[146]~=111236 then aN else(if co[1]<cp[1]then aN[146]==111236 else aN[39]))
	cr = cs[1]
	aN[540][1][1] = cr
	if cs[1] then
	dG = 615128
	do local dN;dN=aN[540][3][1];aN[540][3][1]=aV[1];aV[1]=dN;end
	kY = true
	ct = 1432343
	cu = 656663
	dC = 920651
	else
	dG = 612277
	cl,cp[1],aN[540][3][1],cm[1],cq[1],cn[1]=aN[540][3][1],aV[1],cp[1],cq[1],cm[1],cl
	kY = true
	ct = 920651
	cu = 658944
	dC = 920651
	end
	aU[1] = fI[1]
	cq[1] = nil
	kY = true
	ct,cu=(dG-871)+(310584+871),dG+54571
	cr = 1
	aU[1] = 2915233
	cn[1] = {56, 216, 113, 233, 124}
	aN[540][2][1] = {1827305, 2455699, 51, 55, 171}
	cl = ""
	local dN
	dN = {1827305, 2455699, 51, 55, 171}
	aN[540][2][1] = 2915233
	aU[1] = nil
	cm[1] = {1827305, 2455699, 51, 55, 171}
	dN = nil
	aY[1] = nil
	cg = nil
	kY = true
	cu = 407743
	cl = "table"
	fm = "table"
	kY = true
	ct,cu=(dG-756)+(829502+756),dG+98736
	if kX==nil then
	aW[1] = 5944951
	cr = 1
	cq[1] = {224, 150, 81, 168, 103, 54}
	cm[1] = {772009, 2007861, 147, 69, 13}
	cl = ""
	end
	local dN
	dN = nil
	aN[540][4][1] = nil
	aY[1] = 1
	cr = co[1]
	co[1] = nil
	kY = true
	ct,cu=dG+483250,79776+dG
	cq[1] = {1074737, 1518835, 5, 237, 85}
	cr = 1
	cn[1] = {16, 220, 28, 163, 18, 225}
	cl = ""
	aU[1] = 11826224
	local dN
	dN = nil
	cg = {}
	aV[1] = nil
	dN = nil
	cj = aN[540][1][1]
	aN[540][1][1] = nil
	kY = true
	cu = 504924
	cl = "insert"
	fb = "insert"
	local dN
	aN[540][2][1] = {1074737, 1518835, 5, 237, 85}
	aN[540][4][1] = cj
	dN = nil
	aN[540][1][1] = nil
	ck = nil
	kY = true
	cu = 434802
	kY = true
	cu = 509600
	aN[40] = "format"
	aN[200] = string[aN[40]]
	local dN
	aY[1] = nil
	cj = nil
	aN[540][3][1] = nil
	cm[1] = "insert"
	kY = true
	ct,cu=(dG-197)+(661290+197),dG+1737
	cr = 1
	cn[1] = {1732805, 7045, 201, 51, 155}
	aU[1] = 6685944
	aX[1] = {39, 182, 232, 183}
	cl = ""
	kY = true
	cu = 512621
	cl = "acks"
	eP = "acks"
	local dN
	dN = {1074737, 1518835, 5, 237, 85}
	aV[1] = cs[1]
	cs[1] = {1074737, 1518835, 5, 237, 85}
	dN = {1732805, 7045, 201, 51, 155}
	cn[1] = {39, 182, 232, 183}
	cq[1] = {1732805, 7045, 201, 51, 155}
	dN = nil
	cj = 64
	ci[1] = nil
	kY = true
	ct,cu=285270+dG,48493+dG
	aN[540][4][1] = getfenv[fm]
	aW[1] = "insert"
	aN[540][3][1] = "insert"
	local ld,li=aN[540][4][1],aN[540][3][1]
	aN[540][1][1] = ld[li]
	cn[1] = getfenv[fm]
	co[1] = nil
	co[1] = (if aN[146]~=111236 then aN[576]else kX)
	kY = true
	ct,cu=dG+651444,13603+dG
	local ln,lo=cn[1],co[1]
	cm[1] = ln[lo]
	cj = fI[1]
	ch[1] = "acks"
	aY[1] = (if not aN[21]then aN[549]else cj)[(if not aN[39]then ch[1]else aN[575])]
	cs[1] = aN[540][1][1](aN[540][2][1],cm[1](aY[1]))
	local dN
	cr = 1
	aN[540][3][1] = "acks"
	cf = cs[1]
	cp[1] = "insert"
	cl = {}
	cs[1] = aN[540][1][1]
	aN[540][1][1] = cn[1]
	cg = {1732805, 7045, 201, 51, 155}
	cq[1] = cm[1]
	cm[1] = aV[1]
	aV[1] = aN[540][2][1]
	aN[540][2][1] = {1827305, 2455699, 51, 55, 171}
	ck = cj
	dN = 6685944
	aU[1] = co[1]
	co[1] = aN[540][4][1]
	aN[540][4][1] = 6685944
	dN = "insert"
	aW[1] = nil
	ci[1] = "insert"
	kY = true
	ct,cu=(dG-149)+(822276+149),dG+44296
	return nil
	if kX==nil then
	cl = cb(cq[1],cm[1],aW[1])
	kX = {}
	end
	local dN
	dN = co[1]
	co[1] = {1732805, 7045, 201, 51, 155}
	cg = dN
	dN = 6685944
	aN[540][4][1] = cq[1]
	cq[1] = 6685944
	dN = cf
	cf = aN[540][1][1]
	aN[540][1][1] = dN
	kY = true
	ct,cu=822276+dG,48418+dG
	co[1] = {}
	aV[1] = {}
	local dN
	dN = nil
	aW[1] = aY[1]
	aY[1] = "insert"
	cp[1] = {1827305, 2455699, 51, 55, 171}
	aN[540][2][1] = nil
	kY = true
	ct,cu=dG+822276,dG+44296
	aN[910] = 111575
	co[1] = (if not aN[39]then#aV[1]else aN[567])
	ci[1] = 64
	cp[1] = 64
	cs[1] = co[1]<cp[1]
	cr = (if aN[39]then aN[568]else cs[1])
	aN[540][1][1] = nil
	aN[540][1][1] = (if aN[39]then aN[588]else cr)
	if not cs[1] then
	dG = 612258
	do local dN;cn[1]=cl;cl=aN[540][3][1];aN[540][3][1]=cp[1];cp[1]=aV[1];dN=cq[1];cq[1]=cm[1];cm[1]=dN;end
	kY = true
	ct = 920651
	cu = 658944
	dC = 920651
	else
	dG = 610199
	do local dN;dN=aV[1];aV[1]=aN[540][3][1];aN[540][3][1]=dN;end
	kY = true
	ct = 1432343
	cu = 656663
	dC = 920651
	end
	aU[1] = fI[1]
	cq[1] = "acks"
	local dN
	cn[1] = {}
	dN = cm[1]
	cm[1] = "acks"
	cq[1] = dN
	kY = true
	cu = 664638
	repeat local lp,lq=aU[1],cm[1];ck=lp[lq];cn[1]=#ck;aY[1]=0;cf=aY[1]<cn[1];cr=(if not aN[39]then cf else aN[561]);aN[540][1][1]=cr;dG=(35639+dG);dG=(dG+3144);cl,cp[1],aN[540][3][1],cn[1]=cn[1],aN[540][3][1],cp[1],cl;kY=true;ct=(dG-757)+(310584+757);cu=dG+48877;dC=ct;until aN[21]
	if not aN[540][1][1] then
	dG = 611170
	do local dN;aV[1]=cg;cj=ck;ck=aN[540][2][1];dN=ci[1];ci[1]=aW[1];aW[1]=dN;dN=cn[1];cn[1]=aN[540][1][1];aN[540][1][1]=cs[1];cs[1]=cf;cf=dN;end
	kY = true
	ct = 1804015
	cu = 668918
	dC = 920651
	else
	dG = 619279
	do local dN;dN=cn[1];cn[1]=aN[540][1][1];aN[540][1][1]=dN;dN=ci[1];ci[1]=aW[1];aW[1]=dN;end
	kY = true
	ct,cu=dG+1401561,dG+2022
	dC = 920651
	end
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @9108
	aU = aK
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @11546
	return kW(aN[534][11],fu,fv,aN[534][14],aN[534][6],aW,fw,aN[534][4],aX,dJ,aY,fx,aN[534][18],ck,aN[534][17],aN[534][12],cu,dC,aN[534][9],co,cC,cx,dE,...)end
	dE[1] = 1
	fD = 274260
	aN[534][2][1] = function(...)local jG=function(...)
	-- for-dispatch over gd=66..210 step 4
	aN = {}
	aN[70+611]=70+176
	aH = 352
	aM = true
	aN[82+790]=82~=90
	aN[(86-86)+849]=86+8360
	aN[90+11]=not false
	aN[(730+366)-366]=94~=102
	aN[(98-98)+727]=98+4796
	aN[(62+371)-371]=652567
	aN[106+585]=106+3843
	aN[(110-110)+651]=110~=190
	aN[(874+49)-49]=114+6622
	aN[118+664]=118+7348
	aN[122+748]=122+2562
	aN[(126-126)+770]=126+2435
	aN[(130-130)+876]=130~=90
	aN[(134-134)+775]=134+6223
	aN[667] = 2169
	aN[612] = 5481
	aN[(862+425)-425]=146+7778
	aN[150+510]=150+2587
	aN[154+630]=154+6428
	aN[(861+305)-305]=158+5754
	aN[(806+470)-470]=162+7659
	aN[663] = 549
	aN[(170-170)+4]=not true
	aN[174+515]=174+3071
	aN[(178-178)+790]=178~=118
	aN[182+554]=182~=86
	aN[186+504]=186~=94
	aN[(809+411)-411]=194+3408
	aN[198+437]=198+1692
	aK = function(...)
	ch[1] = fW
	aV[1] = {407269, 866925, 117, 191, 9}
	aU[1] = 1
	cx[1] = ""
	ck[1] = 14712423
	cs[1] = {215, 23, 79, 247, 99}
	ls = true
	cx[1] = "yield"
	bX = "yield"
	local dN
	cC[1] = nil
	dN = 14712423
	ck[1] = {215, 23, 79, 247, 99}
	cs[1] = 14712423
	ls = true
	cx[1] = ""
	ck[1] = {192, 229, 148, 227, 130, 248}
	cs[1] = 1854752
	aV[1] = {3640181, 1802257, 149, 77, 197}
	aU[1] = 1
	ls = true
	cx[1] = "ipairs"
	lr = "ipairs"
	ls = true
	aU[1] = 1
	cx[1] = ""
	cs[1] = 792879
	aN[411][4][1] = {130, 167, 173, 26, 188, 248}
	aV[1] = {2425, 95269, 199, 235, 229}
	local dN
	dN = nil
	cC[1] = nil
	cg[1] = nil
	dN = nil
	cf[1] = nil
	cp[1] = nil
	ls = true
	cx[1] = "insert"
	fb = "insert"
	ls = true
	aV[1] = {1637609, 2213819, 37, 139, 51}
	cs[1] = 1306280
	cx[1] = ""
	aU[1] = {61, 207, 190, 203, 129, 213, 246, 22, 19}
	aN[411][4][1] = 1
	local dN
	cn[1] = 1
	cq[1] = aN[411][1][1]
	aN[411][1][1] = 1306280
	dN = nil
	aN[411][3][1] = 1
	aN[411][4][1] = nil
	ls = true
	cx[1] = "coroutine"
	by = "coroutine"
	ls = true
	cx[1] = ""
	aV[1] = {1663433, 2261299, 123, 165, 207}
	ci = {172, 215, 71, 208}
	aN[411][3][1] = 1
	aN[411][1][1] = 7737010
	local dN
	cm[1] = nil
	cg[1] = {1663433, 2261299, 123, 165, 207}
	aV[1] = 1
	ls = true
	cx[1] = "wrap"
	bW = "wrap"
	ls = true
	cg[1] = {3575373, 589959, 159, 193, 219}
	cx[1] = ""
	ci = {18, 183, 74, 3, 70}
	aN[411][1][1] = 2374285
	aN[411][3][1] = 1
	local dN
	ct[1] = nil
	aN[411][2][1] = nil
	cn[1] = nil
	dN = nil
	dC[1] = nil
	co = nil
	dN = nil
	aX = {3575373, 589959, 159, 193, 219}
	cg[1] = nil
	dN = ck[1]
	ck[1] = nil
	cu = dN
	ls = true
	cx[1] = "table"
	fm = "table"
	ls = true
	co = getfenv[lr]
	aV[1],cf[1],cp[1]=co(cm[1])
	ck[1] = (function(lt,lu,lv,ly)return ly[bW](function()for lB,lC in lt,lu,lv do ly[bX](lB,lC)end end)end)(aV[1],cf[1],cp[1],getfenv[by])
	local dN
	cC[1] = co
	co = nil
	aW = ck[1]
	cs[1] = nil
	ls = true
	cq[1],aX=aW()
	aN[411][2][1] = nil
	cu = nil
	cn[1] = nil
	cn[1] = nil
	cg[1] = true
	cj = true
	local lD=cj
	ls = true
	local dN
	ck[1] = nil
	aN[411][2][1] = "table"
	aN[411][4][1] = cC[1]
	cC[1] = true
	cg[1] = "table"
	dN = nil
	cr[1] = nil
	aN[411][3][1] = nil
	co = nil
	dN = true
	cs[1] = nil
	cj = nil
	aX = true
	ls = true
	ls = true
	aN[1035] = aN[62]+130
	cu = getfenv[fm]
	cs[1] = "insert"
	ct[1] = cu[cs[1]]
	ch[1] = fv[1]
	dC[1] = nil
	dC[1] = nil
	local lG,lJ=ch[1],dC[1]
	aN[411][3][1] = lG[lJ]
	aU[1] = (if aN[62]==652567 then ct[1]else aN[417])(aN[411][3][1],aX)
	ls = true
	if aN[62]==652567 then
	fs = 1095239
	return
	else
	aN[919] = nil
	end
	aN[226] = getfenv
	aN[60] = string
	aN[148] = string.char
	local dN
	dN = ct[1]
	ct[1] = nil
	cm[1] = dN
	dN = nil
	co = nil
	cl[1] = nil
	ls = true
	aN[165] = "format"
	aN[199] = string[aN[165]]
	ls = true
	cx[1] = ""
	ci = {3443541, 3055139, 25, 159, 137}
	aU[1] = 1
	cs[1] = {9, 231, 118, 197}
	cm[1] = 12384118
	local dN
	aN[411][1][1] = nil
	dN = nil
	ck[1] = 12384118
	cm[1] = nil
	dN = nil
	cf[1] = aN[411][2][1]
	aN[411][2][1] = nil
	ls = true
	cx[1] = "acks"
	eP = "acks"
	ls = true
	-- region end
	-- warn: no leaf for key (1830844, 19830)
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @8723
	ci = aK
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @11021
	return jG(aN[534][11],fu,fv,aN[534][14],aN[534][6],aW,fw,aN[534][4],aX,dJ,aY,fx,aN[534][18],ck,aN[534][17],aN[534][12],cu,dC,aN[534][9],cm,co,cC,cx,dE,...)end
	fD = 266515
	fD = 268264
	cf,ch[1],aN[534][22][1],cn=ch[1],cf,cn,aN[534][22][1]
	fE = true
	fF,fG=372293+fD,68655+fD
	fJ = 582328
	end end else
	-- sub-region (fF,fG) base fD:
	local lK=(if not aN[30]then aN[557]else aN[534][23][1])
	aN[534][10][1] = lK(fs[1])
	aN[534][22][1] = nil
	-- sub-region (fF,fG) base fD:
	aN[534][13][1] = nil
	aN[534][13][1] = nil
	cA = nil
	ch[1] = nil
	cq[1] = (if cu[1]==ch[1]then not aN[223]else not aN[30])
	cf = (if cq[1]then aN[223]else aN[85]==631730)
	aN[534][15][1] = cf
	fE = true
	if not((fF-fD)>1272165)then if not((fF-fD)>=1247112)then if(fF-fD)==1240318 then if(fG-fD)==99725 then if bA==nil then aN[534][7][1]=1;cq[1]='';aN[534][23][1]={55,(96+22)-22,191,(28+8)-8,153};aN[534][8][1]={((fD+3011854)-(fD+138241)),((fD+3818486)-(fD+86495)),((fD+388294)-(fD+388213)),((fD+816783)-(fD+816678)),((fD+113462)-(fD+113251))};aN[534][1][1]=((fD+5877599)-(fD+212404));end;fD=(9913+fD);fD=(5336+fD);do local dN;dN=cr[1];cr[1]=aU[1];aU[1]=dN;end;fE=true;fF,fG=(fD-225)+(457936+225),(fD-689)+(8624+689);fJ=fF;end end else if not((fF-fD)>=1255731)then if 63873==(fG-fD)then aY[1]=aN[534][12][1];aN[534][11][1]=(if not aN[30]then aN[585]else aN[572]);aN[534][11][1]=(if not aN[223]then aN[54][fg]else aN[553]);dJ[1]=eU;local lL,lM=aN[534][11][1],dJ[1];aN[534][12][1]=lL[lM];cC[1]=aN[534][12][1]();dJ[1]=(if aN[85]~=631730 then aN[538]else(597440+(-597440)));fD=(fD+29059);aN[534][11][1]=dJ[1];aN[534][12][1]={};aN[534][9][1]=ff;fD=(fD+15854);cx[1]=(if aN[223]then aN[572]else(313677+(-313677)));(if aN[223]then aN else aN[534][12][1])[(if aN[30]then aN[534][9][1]else aN)]=cx[1];aN[534][9][1]=(if not aN[30]then aN[548]else aN);aN[534][9][1]=(if aN[223]then aN else eP);cx[1]={};aN[534][12][1][aN[534][9][1]]=(if not aN[223]then cx[1]else aN[595]);fD=27886+fD;aN[534][9][1]=fn;fD=(fD+715);cx[1]=aN[85]~=631730;fD=fD+4434;local lP,iB,iC=aN[534][12][1],aN[534][9][1],cx[1];lP[iB]=iC;fD=(fD+6563);aN[534][9][1]=(if aN[85]~=631730 then aN[536]else eX);cx[1]=false;fD=6878+fD;(if not aN[223]then aN[534][12][1]else aN[551])[(if not aN[223]then aN[534][9][1]else aN[586])]=cx[1];aN[534][9][1]=eR;aN[534][13][1]=aN[223];fD=fD+15545;fD=7412+fD;do local dN;dN=aV;aV=aN[534][23][1];aN[534][23][1]=dN;dN=fr[1];fr[1]=cf;cf=dN;dN=ch[1];ch[1]=cr[1];cr[1]=dN;end;fE=true;fF,fG=fD+1247112,(fD-12)+(17240+12);fJ=fF;elseif 17240==(fG-fD)then cx[1]=aN[534][13][1];aN[534][12][1][aN[534][9][1]]=(if aN[30]then cx[1]else aN[557]);aN[534][13][1]=(if aN[30]then aN[592]else aN);aN[534][13][1]=(if aN[85]~=631730 then aN[591]else fi);fD=(fD+12772);aN[534][20][1]=aN[534][13][1];fD=(2349+fD);aN[534][9][1],cx[1]=aN[534][20][1],not aN[30];(if aN[223]then aN[587]else aN[534][12][1])[(if not aN[223]then aN[534][9][1]else aN[593])]=cx[1];aN[534][9][1]=(if aN[85]~=631730 then aN[582]else aN);aN[534][9][1]=(if aN[85]~=631730 then aN[544]else fc);fD=(21605+fD);cx[1]=aN[54][fg];aN[534][13][1]=eU;aN[534][6][1]=aN[534][13][1];aN[534][17][1]=cx[1][aN[534][6][1]];ck[1]=aN[534][17][1]();(if not aN[223]then aN[534][12][1]else aN[546])[(if not aN[30]then aN else aN[534][9][1])]=ck[1];aN[534][9][1]=(if aN[85]~=631730 then aN[568]else aN[593]);aN[534][9][1]=(if not aN[30]then aN[563]else fa);cx[1]=(if aN[85]~=631730 then aN[541]else aN);cx[1]=(if not aN[30]then aN[569]else(527471+(-527471)));(if aN[85]~=631730 then aN[534]else aN[534][12][1])[(if aN[223]then aN[539]else aN[534][9][1])]=cx[1];fD=(52396+fD);fD=fD+74;do local dN;aU[1]=aN[534][20][1];dN=aV;aV=aN[534][21][1];aN[534][21][1]=cA;cA=dN;end;fE=true;fF,fG=fD+1247112,fD+6046;fJ=fF;elseif 6046==(fG-fD)then aN[534][9][1]=eT;fD=(fD+5781);cx[1]=aN[85]~=631730;fD=fD+3874;fD=(8119+fD);do local dN;dN=cA;cA=fr[1];fr[1]=dN;end;fE=true;fF=fD+1247112;fG=90318+fD;fJ=fF;elseif(fG-fD)==90318 then aN[534][12][1][aN[534][9][1]]=cx[1];dJ[1]=aN[534][12][1];fD=(fD+6873);aN[534][9][1]=function(...)local lQ=function(...)
	-- for-dispatch over fX=602..497 step -3
	aH = 1
	aN = {}
	aN[(596-596)+811]=596~=587
	aH = 694
	aM = true
	aN[673] = 3549
	aN[584+180]=584+3648
	aN[581+20]=581+9136
	aN[578+289]=578+4180
	aN[(140+303)-303]=false
	aN[(572-572)+685]=572~=602
	aN[569+245]=569+2570
	aN[566+215]=566+4796
	aN[(563-563)+837]=563+2961
	aN[560+44]=560+3219
	aN[557+208]=557~=497
	aN[(796+256)-256]=554~=509
	aN[551+52]=551+7317
	aN[548+177]=548+5869
	aN[776] = 9492
	aN[(772+258)-258]=542+8831
	aN[(789+254)-254]=539+2844
	aN[(756+378)-378]=536+4289
	aN[533+250]=533+3147
	aN[(19+479)-479]=true
	aN[770] = 1200
	aN[524-297]=255365
	aN[(521-521)+720]=521+1501
	aN[(518-518)+804]=518+5310
	aN[515+147]=515+6512
	aN[(512-512)+774]=512+3011
	aN[509+301]=509+7322
	aN[(506-506)+869]=506+8228
	aK = function(...)
	cn = fu
	ci = fv
	-- REGION missing init pair (ct,cq)
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @6898
	aI = aK
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @9119
	return lQ(aN[534][11],fu,fv,aN[534][14],aW,fw,aN[534][4],aX,dJ,aY,fx,aN[534][18],aN[534][12],cu,dC,co,cC,...)end
	aN[534][12][1] = nil
	fD = 265550
	cx[1] = function(...)local gy=function(...)
	-- for-dispatch over mq=234..110 step -4
	aH = 1
	aH = 1
	aN = {}
	aN[222+570]=222+5030
	aH = 456
	aN[(214-214)+708]=214+6840
	aM = true
	aN[206+643]=206~=146
	aN[202+627]=202+8294
	aN[153] = true
	aN[194+484]=194+9597
	aN[865] = 8003
	aN[(186-186)+638]=186+6770
	aN[(182-182)+615]=182+4962
	aN[29] = 796739
	aN[(174-174)+893]=174+3800
	aN[(626+115)-115]=170~=226
	aN[166+555]=166+9665
	aN[743] = 1496
	aN[158-109]=158~=158
	aN[861] = true
	aN[150+662]=150~=190
	aN[732] = 3663
	aN[(142-142)+807]=142+8205
	aN[138+473]=138~=154
	aN[134+666]=134+8990
	aN[740] = 9459
	aN[122+500]=122+4453
	aM = function(...)
	aX[1] = fy
	aU[1] = fz
	ch[1] = fA
	cl[1] = fB
	cn[1] = fC
	cm[1] = fP
	repeat aN[67]=getfenv();aN[161]=string;aN[7]=string.char;dE=(8398+dE);dE=(dE+2533);cq[1],aV[1],cr[1],cp,aN[510][2][1]=aV[1],cq[1],cp,cg,cr[1];mr=true;cs,ct=(dE-533)+(1813799+533),7121+dE;cC=cs;until aN[153]
	cj = cb(aN[510][2][1],cf[1],cp)
	bR = cj
	local dN
	dN = cj
	cj = nil
	cp = dN
	dN = nil
	cr[1] = ci[1]
	ci[1] = nil
	mr = true
	cs,ct=(dE-921)+(691456+921),15761+dE
	cf[1] = {1993129, 700887, 247, 93, 93}
	cj = 13522164
	aN[510][2][1] = {224, 189, 158, 136, 115}
	cr[1] = 1
	cp = ""
	mr = true
	cs,ct=691456+dE,(dE-900)+(40003+900)
	aW[1] = "spawn"
	fk = "spawn"
	local dN
	aN[510][3][1] = {1993129, 700887, 247, 93, 93}
	dN = {79, 251, 6, 169, 61, 135}
	cp = nil
	ci[1] = {79, 251, 6, 169, 61, 135}
	dN = co[1]
	co[1] = {224, 189, 158, 136, 115}
	aN[510][2][1] = dN
	dN = aY[1]
	aY[1] = 12872556
	aV[1] = dN
	mr = true
	ct = 370950
	cq[1] = aN[67][bR]
	aV[1] = "spawn"
	aN[510][2][1] = "spawn"
	local lL,lM=cq[1],aN[510][2][1]
	aY[1] = lL[lM]
	cp = function(...)local jM=function(...)
	-- for-dispatch over ms=426..366 step -2
	aN = {}
	aH = 1307
	aM = true
	aN[(610+168)-168]=420+4499
	aN[418+236]=418+2078
	aN[416+472]=416+1481
	aN[414-187]=not true
	aN[(754+167)-167]=412+7122
	aN[(410-410)+823]=410+1793
	aN[(233+114)-114]=true
	aN[406+292]=406+497
	aN[(793+2)-2]=404+3586
	aN[678] = 6259
	aN[400+395]=400+6089
	aN[784] = true
	aN[(396-396)+653]=396+4145
	aN[(394-394)+691]=394+8124
	aN[392+330]=392+8935
	aN[740] = true
	aN[388+413]=388+9152
	aN[386+512]=386~=380
	aN[764] = 8007
	aN[(382-382)+663]=382+1677
	aN[380+291]=380+9502
	aN[(378-378)+158]=388244
	aN[(761+253)-253]=376~=422
	aN[(894+79)-79]=374~=398
	aN[(630+82)-82]=372+5296
	aL = function(...)
	aN[60] = getfenv
	aN[4] = string
	aN[213] = string.char
	mt = true
	cj = 1576722
	if aN[158]==388244 then
	aN[7] = "format"
	aN[70] = string[aN[7]]
	cp = 839682
	cp = 838343
	ch,aN[522][1][1],aV[1],aW,ci[1]=ci[1],aV[1],aW,aN[522][1][1],ch
	mt = true
	cj = 1608939
	ck = 884653
	cn = 1593499
	else
	aN[1079] = nil
	end
	aN[522][1][1] = {2121749, 525957, 165, 161, 175}
	aW = 1
	ci[1] = ""
	aV[1] = 13577151
	ch = {143, 210, 21, 173, 88}
	local dN
	aN[522][3][1] = {2121749, 525957, 165, 161, 175}
	aN[522][1][1] = 1
	dN = cg[1]
	cg[1] = 13577151
	aV[1] = dN
	mt = true
	cj,ck=(cp-380)+(774624+380),(cp-328)+(69735+328)
	aN[961] = aN[158]+316
	ci[1] = "pcall"
	bK = "pcall"
	mt = true
	cj = 1593499
	aV[1] = getfenv[bK]
	cf[1] = (function(ey,ez,eA,eB,mu,mv,mw,iW,iX,iY,iZ,je,jf,jg,jh,ji,jj,jk,jl,jm,jn,jo,jp,jq)return function(...)return(function(...)
	-- for-dispatch over gg=701..440 step -9
	aH = 0
	aH = 0
	aN = {}
	aN[(769+53)-53]=665+9161
	aH = 1518
	aM = true
	aN[(732+112)-112]=638+9649
	aN[716] = 1540
	aN[(751+391)-391]=620+4897
	aN[611-588]=false
	aN[95] = 373714
	aN[593+90]=593+3201
	aN[584+214]=584+6165
	aN[566+154]=566+5406
	aN[(618+395)-395]=557+9896
	aN[(548-548)+37]=not false
	aN[(539-539)+712]=539+8193
	aN[(705+170)-170]=530+4574
	aN[731] = 6996
	aN[(512-512)+670]=512~=566
	aN[503+202]=503+9563
	aN[(494-494)+706]=494+9515
	aN[485+189]=485+8302
	aN[476+219]=476+9665
	aN[467+372]=467+5951
	aH = function(...)
	aN[80] = getfenv
	aN[131] = string
	aN[113] = string.char
	local dN
	dN = nil
	dG[1] = aY[1]
	aY[1] = nil
	cs[1] = nil
	dN = nil
	cj = cn[1]
	cn[1] = nil
	fE = true
	aN[141] = "format"
	aN[155] = string[aN[141]]
	fE = true
	cg[1] = {86, 62, 114, 53, 54, 34, 219, 170, 111, 40}
	cm = ""
	dG[1] = 1
	cr[1] = 9591538
	cl = {603113, 83079, 41, 29, 51}
	fE = true
	ci[1] = "connection"
	mx = "connection"
	fE = true
	cg[1] = {250}
	ci[1] = ""
	cl = {1989229, 2586889, 99, 89, 3}
	cr[1] = 6582573
	dG[1] = 1
	local dN
	aN[335][6][1] = aV[1]
	dN = aX[1]
	aX[1] = {250}
	cg[1] = dN
	dN = 1
	dG[1] = "spawn"
	ck[1] = 1
	fE = true
	ci[1] = "e"
	bB = "e"
	fE = true
	aX[1] = {186, 190, 118, 20, 180}
	cr[1] = 11789334
	ci[1] = ""
	cl = {754033, 1424051, 105, 1, 99}
	ck[1] = 1
	local dN
	aN[335][8][1] = "spawn"
	dN = nil
	cs[1] = nil
	ft = nil
	dN = cg[1]
	cg[1] = nil
	fr[1] = dN
	fE = true
	ci[1] = "clock"
	eU = "clock"
	fE = true
	ci[1] = ""
	cl = {93473, 632693, 59, 253, 65}
	aX[1] = {203, 211, 47, 170}
	cr[1] = 11895673
	ck[1] = 1
	fE = true
	ci[1] = "math"
	fd = "math"
	local dN
	aW[1] = aN[335][6][1]
	aN[335][6][1] = nil
	dN = "pcall"
	dC[1] = fr[1]
	fr[1] = "pcall"
	dN = nil
	ft = nil
	fs[1] = nil
	fE = true
	aX[1] = {41}
	ci[1] = ""
	cl = {695357, 244307, 127, 237, 237}
	ck[1] = 1
	cr[1] = 4399212
	fE = true
	ci[1] = "g"
	mz = "g"
	fE = true
	cl = {3805785, 940585, 33, 203, 115}
	ck[1] = 1
	ci[1] = ""
	cr[1] = 9017096
	cA = {182}
	fE = true
	ci[1] = "a"
	bv = "a"
	fE = true
	cr[1] = 15609326
	ci[1] = ""
	cs[1] = {136, 111, 73}
	cl = {3701705, 1368607, 113, 35, 239}
	cC[1] = 1
	fE = true
	ci[1] = "min"
	fe = "min"
	local dN
	cg[1] = fs[1]
	fs[1] = {224, 189, 158, 136, 115}
	dE[1] = nil
	dN = nil
	cA = nil
	aW[1] = nil
	dN = nil
	co[1] = nil
	cf = nil
	dN = dC[1]
	dC[1] = nil
	ct = dN
	fE = true
	ci[1] = ""
	cC[1] = 1
	cs[1] = {147, 254, 91, 220, 189, 152, 9, 255, 117, 159}
	cr[1] = 15235759
	aN[335][6][1] = {1824601, 1508477, 73, 143, 111}
	fE = true
	ci[1] = "JSONEncode"
	eJ = "JSONEncode"
	fE = true
	cj = 1165837
	cs[1] = {181, 172, 0, 189, 36, 84, 199, 217, 254, 15, 62, 36, 212, 41, 94, 40, 144, 4, 82, 205, 109, 98, 237, 70, 225, 2, 213, 56, 18, 12, 96, 230, 125, 238, 168, 37, 219, 254, 55, 108, 53, 129, 14, 36, 57, 52, 17, 59}
	ci[1] = ""
	cC[1] = 1
	aN[335][6][1] = {2711269, 365943, 117, 1, 131}
	local dN
	cr[1] = nil
	dN = nil
	cu = nil
	dG[1] = nil
	fE = true
	ci[1] = "https://api.polsec.net/runtime/socket/diagnostic"
	mB = "https://api.polsec.net/runtime/socket/diagnostic"
	local dN
	cx[1] = nil
	ch[1] = "spawn"
	aN[335][5][1] = nil
	dN = "pcall"
	aY[1] = cq[1]
	cq[1] = "pcall"
	fE = true
	aN[335][6][1] = {698165, 414811, 137, 191, 235}
	cs[1] = {5}
	cj = 8151256
	cC[1] = 1
	ci[1] = ""
	fE = true
	ci[1] = "j"
	mD = "j"
	fE = true
	cs[1] = {8, 130}
	ci[1] = 1
	aN[335][7][1] = ""
	cx[1] = {3882885, 1925231, 175, 133, 75}
	cj = 14700409
	local dN
	dC[1] = nil
	cC[1] = nil
	cA = nil
	dN = aY[1]
	aY[1] = nil
	cr[1] = dN
	fE = true
	aN[335][7][1] = "os"
	fg = "os"
	local dN
	ck[1] = nil
	aN[335][6][1] = dL
	cm = {8, 130}
	dN = nil
	cf = nil
	cg[1] = "spawn"
	ft = nil
	fE = true
	cm = {40}
	cx[1] = {1819281, 3651427, 9, 197, 137}
	aN[335][7][1] = ""
	ci[1] = 1
	cj = 5414409
	local dN
	cp = cr[1]
	dL = {1819281, 3651427, 9, 197, 137}
	aU = nil
	cA = ""
	dN = "pcall"
	cq[1] = aN[335][6][1]
	aN[335][6][1] = nil
	aN[335][5][1] = "pcall"
	fE = true
	cA = "f"
	eW = "f"
	local dN
	cr[1] = nil
	cs[1] = ct
	dN = nil
	ck[1] = "f"
	cA = nil
	fE = true
	ci[1] = 1
	dL = {3282621, 2333247, 249, 197, 15}
	cm = {212}
	cj = 11404222
	ck[1] = ""
	local dN
	cx[1] = {224, 189, 158, 136, 115}
	aX[1] = 11404222
	dN = nil
	aV[1] = nil
	cu = nil
	dN = nil
	cn[1] = nil
	aN[335][6][1] = "spawn"
	cg[1] = nil
	fE = true
	while aN[23]do aN[1050]=aN[95];end
	ck[1] = "d"
	bz = "d"
	fE = true
	cm = {245, 219, 6}
	aV[1] = 3636738
	dL = {3402037, 2253051, 193, 191, 127}
	cC[1] = ""
	ci[1] = 1
	local dN
	cl = nil
	aX[1] = "pcall"
	dN = nil
	cu = cs[1]
	cs[1] = nil
	fE = true
	cC[1] = "max"
	mF = "max"
	local dN
	aN[335][7][1] = {245, 219, 6}
	cm = nil
	dN = {3402037, 2253051, 193, 191, 127}
	dL = nil
	cf = {3402037, 2253051, 193, 191, 127}
	dN = cq[1]
	cq[1] = nil
	cl = dN
	fE = true
	aN[335][7][1] = {66}
	cf = {1760717, 235159, 191, 95, 31}
	aV[1] = 14543190
	ci[1] = 1
	cC[1] = ""
	fE = true
	cC[1] = "c"
	bx = "c"
	local dN
	aN[335][6][1] = nil
	aU = nil
	dN = nil
	cs[1] = nil
	cA = "pcall"
	aX[1] = nil
	dN = nil
	aY[1] = fr[1]
	fr[1] = nil
	fE = true
	cf = {3804709, 3734391, 163, 71, 121}
	cC[1] = ""
	dE[1] = 5253326
	aN[335][7][1] = {45, 47, 19, 191, 231}
	ci[1] = 1
	local dN
	dL = 1
	aN[335][5][1] = aY[1]
	dN = nil
	cr[1] = ""
	cC[1] = nil
	dN = "pcall"
	cA = nil
	aU = "pcall"
	dN = nil
	dG[1] = nil
	cs[1] = nil
	fE = true
	cr[1] = "floor"
	my = "floor"
	local dN
	dN = nil
	dJ[1] = nil
	aN[335][8][1] = nil
	fE = true
	dL = 1
	dE[1] = 16008724
	cf = {1868141, 3968695, 237, 155, 81}
	cr[1] = ""
	aN[335][7][1] = {240}
	fE = true
	cr[1] = "b"
	bw = "b"
	fE = true
	aN[1024] = 374437
	dL = 1
	aN[335][7][1] = {110}
	dE[1] = 9911157
	fs[1] = {3693393, 3042417, 167, 27, 33}
	cr[1] = ""
	fE = true
	cr[1] = "i"
	mC = "i"
	local dN
	cg[1] = nil
	dN = {110}
	aN[335][7][1] = nil
	cC[1] = cl
	cl = "i"
	cr[1] = {110}
	fE = true
	aN[1076] = 374071
	if bb==nil then
	cr[1] = {}
	cl = ""
	dL = 1
	dE[1] = 8515591
	cn[1] = {1312737, 943133, 133, 191, 233}
	end
	fE = true
	if bb==nil then
	cl = cc(cr[1],cu,dE[1])
	bb = "b"
	end
	local dN
	dN = nil
	fs[1] = cf
	cf = nil
	dN = nil
	cg[1] = "i"
	cl = nil
	fE = true
	dL = 1
	cu = {1668717, 2838845, 151, 189, 171}
	cg[1] = ""
	dE[1] = 939355
	cr[1] = {123}
	fE = true
	cg[1] = "k"
	mE = "k"
	fE = true
	while aN[23]do aN[991]=aN[95];end
	dE[1] = 12390624
	cr[1] = {146}
	cu = {2710593, 3847255, 73, 21, 81}
	cg[1] = ""
	dL = 1
	fE = true
	repeat if mA==nil then cg[1]=ce(cr[1],cu,dE[1]);mA=cg[1];end;fD=fD+9038;fD=(fD+4471);cq[1],aY[1],dC[1],ft,dJ[1],aX[1],aW[1]=dJ[1],fr[1],aW[1],cq[1],ft,dE[1],dC[1];fE=true;fF,fG=fD+820383,(fD-978)+(6971+978);fJ=fF;until aN[37]
	aN[335][4][1] = gc[1]
	aN[335][2][1] = aN[335][1][1]-aN[335][4][1]
	cf = 1000
	aV[1] = 1000
	ck[1] = aV[1]*aN[335][2][1]
	dL = cs[1](dC[1],ch[1](aN[335][8][1],cA(ck[1])))
	aN[335][5][1][aX[1]]=dL
	aX[1] = nil
	aN[335][7][1] = fT[1]
	aN[335][5][1][aX[1]]=aN[335][7][1]
	cf = "i"
	aX[1] = "i"
	aN[335][7][1] = fP[1]
	aN[335][5][1][aX[1]]=aN[335][7][1]
	cf = "j"
	cj = "j"
	fE = true
	ch[1] = fs[1][aV[1]]
	cr[1] = 0
	co[1] = getfenv[fd]
	cf = "floor"
	cj = "floor"
	aY[1] = "floor"
	cA = co[1][aY[1]]
	ci[1] = getfenv[fg]
	fr[1] = "clock"
	cx[1] = ci[1][fr[1]]
	aN[335][1][1] = cx[1]()
	local dN
	cq[1] = cp
	aN[335][8][1] = 0
	dN = aW[1]
	aW[1] = 1000
	aV[1] = dN
	fE = true
	dL = "floor"
	aN[335][7][1] = fx[1]
	aN[335][5][1][dL]=aN[335][7][1]
	dL = "k"
	aN[335][7][1] = ga[1]
	fE = true
	ch[1] = fW[1]
	ci[1] = "https://api.polsec.net/runtime/socket/diagnostic"
	co[1] = fC[1]
	aN[335][3][1] = "JSONEncode"
	cl = co[1][aN[335][3][1]]
	dJ[1] = {}
	aN[335][8][1] = "a"
	fE = true
	cf = fV[1]
	dC[1][aN[335][8][1]]=cf
	cn[1] = "b"
	aN[335][8][1] = "b"
	cf = fO[1]
	dC[1][aN[335][8][1]]=cf
	aN[335][8][1] = "c"
	cf = fy[1]
	dC[1][aN[335][8][1]]=cf
	local dN
	dN = ch[1]
	ch[1] = 0
	cr[1] = dN
	dN = nil
	aN[335][6][1] = cl
	cl = nil
	fE = true
	cs[1] = fQ[1]
	cq[1] = ""
	fs[1] = ""
	aX[1] = ""
	cj = cs[1]..aX[1]
	ft = cj
	fE = true
	fs[1] = ft
	aV[1] = fs[1]
	cC[1] = not ft
	local dN
	aN[335][7][1] = cf
	ch[1] = aN[335][6][1]
	aN[335][6][1] = "pcall"
	aU = nil
	dN = fs[1]
	fs[1] = cj
	cj = dN
	dN = cC[1]
	cC[1] = "k"
	dL = "b"
	cn[1] = dN
	dN = {224, 189, 158, 136, 115}
	dG[1] = "https://api.polsec.net/runtime/socket/diagnostic"
	ci[1] = {224, 189, 158, 136, 115}
	dN = 1000
	cp = co[1]
	co[1] = 1000
	fE = true
	local dN
	aN[335][6][1] = nil
	aU = nil
	aN[335][5][1] = "c"
	co[1] = cp
	cf = ""
	cp = {2710593, 3847255, 73, 21, 81}
	dN = cj
	cj = fs[1]
	fs[1] = dN
	dN = nil
	dJ[1] = ch[1]
	ch[1] = nil
	fE = true
	dJ[1] = ""
	cj = ""
	aV[1] = ""
	local dN
	cf = ""
	aN[335][5][1] = "c"
	dN = nil
	ch[1] = ""
	dJ[1] = nil
	fE = true
	aN[335][5][1][aX[1]]=aV[1]
	aX[1] = "f"
	aN[335][7][1] = fu[1]
	aN[335][5][1][aX[1]]=aN[335][7][1]
	aX[1] = "g"
	aN[335][7][1] = getfenv[fd]
	ft = "min"
	cs[1] = aN[335][7][1][ft]
	dC[1] = 86400000
	fs[1] = getfenv[fd]
	aV[1] = "max"
	local dN
	dN = cx[1]
	cx[1] = ck[1]
	ck[1] = dN
	dN = "k"
	cC[1] = {224, 189, 158, 136, 115}
	ci[1] = "k"
	dN = nil
	cm = "clock"
	fr[1] = nil
	fE = true
	aN[335][8][1] = "d"
	cf = gb[1]
	dC[1][aN[335][8][1]]=cf
	aN[335][8][1] = "e"
	cf = fQ[1]
	fs[1] = cf
	ft = fs[1]
	cC[1] = not cf
	local mG=cC[1]
	fE = true
	fE = true
	local dN
	dG[1] = "b"
	dL = aN[335][7][1]
	dN = "clock"
	cr[1] = nil
	aU = "clock"
	dN = aX[1]
	aX[1] = "c"
	cA = dN
	dN = 86400000
	aN[335][8][1] = "e"
	dC[1] = 86400000
	fE = true
	aX[1] = aN[335][7][1]
	cn[1] = aX[1]
	ft = not aN[335][7][1]
	local mH=ft
	if nil then
	do local dN;cr[1]=cj;cu=ct;aW[1]=cp;cp=cx[1];cx[1]=cC[1];dN=fs[1];fs[1]=ch[1];ch[1]=dN;end
	else
	do local dN;cu=dL;aW[1]=cp;cs[1]=aN[335][7][1];cp=cx[1];cx[1]=cC[1];aN[335][7][1]=ft;ft=ch[1];ch[1]=fs[1];cr[1]=cj;cj=ct;dN=dG[1];dG[1]=cf;cf=dN;end
	end
	fE = true
	fE = true
	repeat fD=(3288+fD);do local dN;fs[1]=cn[1];dL=aN[335][5][1];cn[1]=ck[1];cC[1]=dE[1];dN=aV[1];aV[1]=dG[1];dG[1]=dN;dN=ft;ft=aW[1];aW[1]=dN;dN=cg[1];cg[1]=cq[1];cq[1]=cx[1];cx[1]=dN;end;fE=true;fF=(fD-796)+(1253311+796);fG=14844+fD;fJ=fF;until aN[37]
	cj = "connection"
	aX[1] = "connection"
	ck[1] = "connection"
	local dN
	dL = "g"
	cC[1] = {2710593, 3847255, 73, 21, 81}
	fs[1] = "connection"
	dN = {2710593, 3847255, 73, 21, 81}
	aW[1] = ft
	ft = {2710593, 3847255, 73, 21, 81}
	dN = ""
	cg[1] = ""
	cx[1] = ""
	fE = true
	dL[cu]=fs[1]
	cu = aN[335][6][1](cm,dJ[1](cg[1],dL))
	return
	aX[1] = aN[335][7][1]
	cn[1] = aX[1]
	ft = not aN[335][7][1]
	local mI=ft
	fE = true
	local dN
	cs[1] = aN[335][7][1]
	aN[335][7][1] = ft
	cj = "g"
	cu = "g"
	ft = "connection"
	dN = cq[1]
	cq[1] = {2710593, 3847255, 73, 21, 81}
	cx[1] = dN
	dN = "max"
	cf = "b"
	dG[1] = aV[1]
	aV[1] = "max"
	dN = cn[1]
	cn[1] = "connection"
	ck[1] = dN
	fE = true
	fE = true
	cj = "connection"
	aX[1] = "connection"
	ck[1] = "connection"
	fE = true
	dL[cu]=fs[1]
	cu = aN[335][6][1](cm,dJ[1](cg[1],dL))
	return
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @24394
	aM = aH
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @26153
	)(ey,ez,eA,eB,mu,mv,mw,iW,iX,iY,iZ,je,jf,jg,jh,ji,jj,jk,jl,jm,jn,jo,jp,jq,...)end end)(cq,cr,cs,ct,cu,cx,cC,dC,dE,dG,dJ,dL,cA,fr,fs,ft,fF,fG,fH,fI,fJ,fK,fD,fu)
	aX[1] = aV[1](cf[1])
	return
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @28326
	aI = aL
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @30312
	return jM(dG,dJ,dL,cn,aX,cA,fr,fs,ft,cl,fF,fG,fH,ch,fI,fJ,fK,fD,fu,fv,fw,cm,aU,fx,...)end
	ci[1] = (if aN[153]then aY[1]else aN[524])(cp)
	return
	aN[77] = aN[7](((213+256-111)-(((213+256-111))//256)*256),((83+256-228)-(((83+256-228))//256)*256),((195+256-81)-(((195+256-81))//256)*256),((165+256-56)-(((165+256-56))//256)*256),((114+256-17)-(((114+256-17))//256)*256),((241+256-125)-(((241+256-125))//256)*256))
	aN[12] = aN[161][aN[77]]
	mr = true
	ct = 389267
	if bR==nil then
	aN[510][2][1] = {146, 158, 103, 138}
	cf[1] = 4358024
	ci[1] = 1
	cj = ""
	cp = {1234381, 3363393, 71, 123, 81}
	end
	mr = true
	ct = 386563
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @33352
	aX = aM
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @35264
	return gy(aN[534][11],fu,fv,aN[534][14],aW,fw,aN[534][4],aX,dJ,aY,fx,aN[534][18],aN[534][12],cu,dC,aN[534][9],co,cC,...)end
	aN[534][9][1] = cx[1]
	fD = 274998
	aN[534][6][1] = function(...)local jL=function(...)
	-- for-dispatch over js=1062..990 step -2
	aH = 1
	aN = {}
	aN[(746+40)-40]=1058+4064
	aN[823] = 3775
	aH = 1947
	aN[725] = 10264
	aN[1050-271]=1050+9690
	aM = true
	aN[1046-372]=1046+5285
	aN[(833+493)-493]=1044~=1054
	aN[(767+19)-19]=1042+2014
	aN[(877+304)-304]=1040+7619
	aN[1038-304]=1038+9779
	aN[(1036-1036)+757]=1036+2907
	aN[1034-194]=1034~=1058
	aN[729] = 2206
	aN[1030-247]=1030+7657
	aN[743] = true
	aN[(637+329)-329]=1026+321
	aN[1024-136]=1024~=1062
	aN[1022-371]=1022+6777
	aN[637] = true
	aN[(882+122)-122]=1018+5466
	aN[(1016-1016)+79]=true
	aN[1014-226]=1014+3733
	aN[(1012-1012)+732]=1012+4775
	aN[160] = 328539
	aN[85] = false
	aN[1006-262]=1006~=1008
	aN[1004-169]=1004+9056
	aN[(742+283)-283]=1002+2529
	aN[1000-392]=1000~=1008
	aN[998-271]=998+8496
	aN[618] = true
	aI = function(...)
	cl[1] = fQ
	ck[1] = fR
	cr[1] = fS
	aU = fT
	aW[1] = fU
	aN[76] = getfenv
	aN[70] = string
	aN[9] = string.char
	local dN
	aN[422][1][1] = nil
	dN = aX[1]
	aX[1] = nil
	cg[1] = dN
	dN = cu[1]
	cu[1] = 1
	cq[1] = dN
	mJ = true
	while aN[85]do aN[1032]=aN[160];end
	aN[191] = "format"
	aN[157] = string[aN[191]]
	local dN
	aN[422][4][1] = nil
	dN = nil
	cl[1] = 1
	cu[1] = nil
	dN = nil
	cj = co[1]
	co[1] = nil
	dN = {79, 251, 6, 169, 61, 135}
	aW[1] = nil
	aX[1] = {79, 251, 6, 169, 61, 135}
	mJ = true
	aN[422][4][1] = ""
	cl[1] = {193, 147, 233, 245}
	cq[1] = 3459414
	cC[1] = 1
	cp[1] = {1822273, 63383, 171, 167, 157}
	local dN
	dN = nil
	cn = nil
	co[1] = nil
	dN = nil
	cf[1] = ci[1]
	ci[1] = nil
	dN = nil
	aU = {193, 147, 233, 245}
	cl[1] = nil
	mJ = true
	aN[422][4][1] = "wait"
	fp = "wait"
	local dN
	aN[422][3][1] = nil
	ch = {1822273, 63383, 171, 167, 157}
	cx = 1
	mJ = true
	aU = {155, 180, 11, 208, 235, 94, 49, 6, 244, 88}
	aN[422][4][1] = ""
	cq[1] = 1536004
	cx = 1
	ch = {265329, 3355001, 191, 87, 123}
	local dN
	dN = nil
	aW[1] = ck[1]
	ck[1] = nil
	mJ = true
	aN[422][4][1] = "GetService"
	bf = "GetService"
	mJ = true
	cq[1] = 14483500
	cx = 1
	ch = {3394233, 740439, 109, 197, 199}
	aN[422][4][1] = ""
	cg[1] = {133, 102, 188, 72, 6, 32, 67, 125, 101, 164, 46}
	mJ = true
	aN[422][4][1] = "LocalPlayer"
	bk = "LocalPlayer"
	mJ = true
	cg[1] = {141, 0, 152, 234}
	cn = 1257210
	cq[1] = 1
	ch = {1654445, 2798165, 153, 171, 131}
	aN[422][4][1] = ""
	local dN
	dN = nil
	aY[1] = {141, 0, 152, 234}
	cg[1] = nil
	dN = nil
	aN[422][2][1] = nil
	cl[1] = nil
	dN = nil
	cp[1] = cs[1]
	cs[1] = nil
	mJ = true
	aN[422][4][1] = "Kick"
	bi = "Kick"
	local dN
	cC[1] = nil
	aN[422][1][1] = 12872556
	dN = {141, 0, 152, 234}
	aY[1] = ck[1]
	ck[1] = {141, 0, 152, 234}
	mJ = true
	ch = {107673, 1587137, 81, 159, 67}
	aN[422][4][1] = ""
	cn = 3387083
	cq[1] = 1
	ck[1] = {201, 231, 169, 92, 158, 204, 169}
	local dN
	aV[1] = nil
	dN = aW[1]
	aW[1] = nil
	cg[1] = dN
	mJ = true
	aN[422][4][1] = "Players"
	bm = "Players"
	mJ = true
	ch = {224001, 3428651, 59, 81, 217}
	ck[1] = {148, 246, 71, 213}
	aN[422][2][1] = ""
	cl[1] = 6319282
	cq[1] = 1
	mJ = true
	aN[422][2][1] = "task"
	bR = "task"
	mJ = true
	cl[1] = 856616
	aN[422][4][1] = {160, 131, 173, 11, 108, 143, 43, 50}
	cq[1] = 1
	ck[1] = {1976497, 1828597, 135, 139, 173}
	aN[422][2][1] = ""
	mJ = true
	cp[1] = "terminal"
	fn = "terminal"
	local dN
	cl[1] = nil
	aW[1] = "terminal"
	dN = nil
	aX[1] = nil
	cC[1] = nil
	mJ = true
	aY[1] = nil
	cl[1] = nil
	aX[1] = fD[1]
	cr[1] = "terminal"
	aX[1][cr[1]]=(if aN[160]~=328539 then aN[482]else cl[1])
	cl[1] = fA[1]
	local mK=(if not aN[85]then cl[1]else aN[433])
	aY[1] = mK(cC[1],cg[1],cn,cs[1],aV[1])
	cl[1] = fI[1]
	aY[1] = "GetService"
	local ib,ic=cl[1],aY[1]
	aX[1] = ib[ic]
	cr[1] = nil
	cr[1] = "Players"
	local mL=aX[1]
	ch = mL(cl[1],cr[1])
	aN[422][1][1] = "LocalPlayer"
	cf[1] = ch[aN[422][1][1]]
	ci[1] = "Kick"
	ct[1] = nil
	aN[422][2][1] = (if aN[85]then aN[477]else cf[1])[(if aN[79]then ct[1]else aN[437])]
	local dN
	co[1] = 1
	cu[1] = nil
	aN[422][3][1] = {160, 131, 173, 11, 108, 143, 43, 50}
	cp[1] = "LocalPlayer"
	aN[422][1][1] = {1976497, 1828597, 135, 139, 173}
	mJ = true
	cm[1] = aN[422][2][1](cf[1],cC[1])
	local dN
	cj = "LocalPlayer"
	dN = "Kick"
	ci[1] = "terminal"
	aW[1] = "Players"
	cr[1] = "Kick"
	mJ = true
	cl[1] = nil
	cl[1] = true
	cu[1] = false
	local mM=cu[1]
	mJ = true
	cl[1] = nil
	cl[1] = (if aN[85]then aN[441]else getfenv[bR])
	cr[1] = "wait"
	aY[1] = "wait"
	cq[1] = cl[1][(if aN[160]==328539 then aY[1]else aN[485])]
	local mN=(if aN[79]then cq[1]else aN)
	aW[1] = mN()
	local dN
	aN[422][4][1] = nil
	cn = 856616
	dN = 1
	co[1] = nil
	cC[1] = 1
	mJ = true
	local dN
	aU = 856616
	ci[1] = "terminal"
	aX[1] = cq[1]
	cn = nil
	dN = nil
	co[1] = 1
	cC[1] = nil
	dN = cj
	cj = "LocalPlayer"
	cm[1] = dN
	mJ = true
	if bi==nil then
	aN[422][4][1] = cb(aY[1],ch,cn)
	bi = aN[422][4][1]
	end
	local dN
	cC[1] = {1976497, 1828597, 135, 139, 173}
	aN[422][1][1] = {160, 131, 173, 11, 108, 143, 43, 50}
	dN = {1976497, 1828597, 135, 139, 173}
	ck[1] = "wait"
	aY[1] = {1976497, 1828597, 135, 139, 173}
	mJ = true
	if bk==nil then
	aN[422][4][1] = ce(cg[1],ch,cq[1])
	bk = aN[422][4][1]
	end
	local dN
	cl[1] = {79, 251, 6, 169, 61, 135}
	dN = nil
	cx = nil
	cn = cq[1]
	cq[1] = nil
	dN = "wait"
	cr[1] = 1
	co[1] = "wait"
	mJ = true
	repeat if bi==nil then cn=((fr+1575809)-(fr+318599));cg[1]={(141-28)+28,0,152,234};ch={((fr+1986381)-(fr+331936)),((fr+3599635)-(fr+801470)),((fr+483575)-(fr+483422)),((fr+101977)-(fr+101806)),((fr+151952)-(fr+151821))};cq[1]=1;aN[422][4][1]='';end;fr=(fr+4551);fr=fr+1988;do local dN;dN=cp[1];cp[1]=cs[1];cs[1]=dN;dN=aY[1];aY[1]=cg[1];cg[1]=dN;dN=aN[422][2][1];aN[422][2][1]=cl[1];cl[1]=dN;end;mJ=true;dC=fr+1000914;dE=fr+56186;dL=dC;until aN[79]
	while aN[85]do aN[942]=aN[160];end
	return
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @10061
	aU = aI
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @12380
	return jL(aN[534][11],fu,fv,aN[534][14],aW,fw,aN[534][4],aX,dJ,aY,fx,aN[534][18],aN[534][12],cu,dC,aN[534][9],co,cC,cx,...)end
	cx[1] = nil
	fD = 268869
	aN[534][17][1] = function(...)local mO=function(...)
	-- for-dispatch over jk=614..690 step 2
	aN = {}
	aN[627] = 9827
	aH = 1428
	aN[(620-620)+836]=620+4271
	aM = true
	aN[(771+141)-141]=624~=678
	aN[626+102]=626~=634
	aN[694] = 2698
	aN[(686+265)-265]=630~=656
	aN[632-1]=632+8226
	aN[774] = 10482
	aN[(636-636)+826]=636+2511
	aN[638+234]=638~=624
	aN[(640-640)+896]=640+1662
	aN[642+235]=642~=648
	aN[644+19]=644+5576
	aN[646+145]=646~=684
	aN[648+163]=648+3938
	aN[650-447]=not false
	aN[654+199]=654+737
	aN[656+128]=656+8814
	aN[762] = 8397
	aN[827] = 8037
	aN[662+225]=662+8911
	aN[(664-664)+751]=664+2269
	aN[(666-666)+753]=666+6293
	aN[(793+310)-310]=668+9684
	aN[(879+448)-448]=670+350
	aN[(676-676)+144]=false
	aN[67] = 230922
	aN[(812+503)-503]=680+6501
	aN[684+131]=684+4736
	aL = function(...)
	cl[1] = fz
	aN[207] = getfenv
	aN[162] = string
	aN[204] = string.char
	mQ = true
	aN[25] = "format"
	aN[74] = string[aN[25]]
	mQ = true
	ci[1] = 1
	aW[1] = ""
	cj[1] = {3582929, 1215115, 197, 57, 23}
	cq[1] = {31, 132, 89, 204, 100, 53, 150, 30, 238}
	aU[1] = 11972545
	mQ = true
	aW[1] = "coroutine"
	by = "coroutine"
	mQ = true
	aV[1] = 13886482
	ci[1] = 1
	aW[1] = ""
	cq[1] = {58, 67, 232, 73, 211}
	cj[1] = {2584681, 3761109, 201, 153, 175}
	mQ = true
	aW[1] = "yield"
	bX = "yield"
	mQ = true
	aN[478][1][1] = 1
	ch = {1813601, 1886425, 65, 39, 75}
	cq[1] = 11895135
	aW[1] = ""
	aN[478][3][1] = {246, 169, 95, 53, 151, 30, 53, 127}
	mQ = true
	aN[926] = 231013
	aW[1] = "tostring"
	mP = "tostring"
	local dN
	dN = {79, 251, 6, 169, 61, 135}
	cj[1] = {246, 169, 95, 53, 151, 30, 53, 127}
	aN[478][3][1] = {79, 251, 6, 169, 61, 135}
	mQ = true
	cf[1] = {377217, 75751, 243, 81, 117}
	aN[478][1][1] = 1
	aW[1] = ""
	cj[1] = {27, 155, 167}
	cq[1] = 6042981
	local dN
	aN[478][4][1] = 12872556
	ck[1] = 1
	dN = {377217, 75751, 243, 81, 117}
	cf[1] = {79, 251, 6, 169, 61, 135}
	aN[478][3][1] = {377217, 75751, 243, 81, 117}
	dN = nil
	cn = nil
	aY = nil
	mQ = true
	aW[1] = "sub"
	fl = "sub"
	mQ = true
	cq[1] = 13748384
	cj[1] = {178, 152, 1, 105, 33}
	aW[1] = ""
	aN[478][3][1] = {2940601, 557121, 19, 65, 59}
	aN[478][1][1] = 1
	local dN
	dN = {178, 152, 1, 105, 33}
	cj[1] = ""
	aW[1] = {178, 152, 1, 105, 33}
	mQ = true
	cj[1] = "pcall"
	bK = "pcall"
	local dN
	dN = 13748384
	cq[1] = nil
	cn = aX[1]
	aX[1] = 13748384
	mQ = true
	cg[1] = (if aN[67]==230922 then getfenv[mP]else aN)
	local mR=(if not aN[144]then cg[1]else aN[513])
	ck[1] = mR(cl[1])
	cp[1] = "sub"
	cq[1] = ck[1][(if aN[67]==230922 then cp[1]else aN)]
	aU[1] = 200
	ci[1] = nil
	ci[1] = nil
	cm[1] = cq[1](ck[1],co[1],ci[1])
	cl[1] = cm[1]
	cm[1] = getfenv[bK]
	cg[1] = function(...)local mS=function(...)
	-- for-dispatch over mT=882..1113 step 7
	aN = {}
	aH = 1422
	aM = true
	aN[903-279]=903+5441
	aN[(749+330)-330]=910+3533
	aN[634] = 1296
	aN[(49+207)-207]=not false
	aN[(709+498)-498]=931+1223
	aN[938-224]=938+8177
	aN[607] = 10664
	aN[952-72]=952~=1085
	aN[959-95]=959~=889
	aN[798] = 3774
	aN[973-188]=973+3562
	aN[(980-980)+761]=980+3848
	aN[27] = 297209
	aN[(841+361)-361]=994+4116
	aN[1001-181]=1001~=931
	aN[616] = true
	aN[(722+317)-317]=1015+6609
	aN[847] = true
	aN[1029-411]=1029+5395
	aN[1036-411]=1036+9723
	aN[(1043-1043)+712]=1043~=910
	aN[1050-216]=1050+9550
	aN[1057-230]=1057+2616
	aN[(687+420)-420]=1064+7035
	aN[1071-270]=1071+1875
	aN[1078-305]=1078+8626
	aN[(1085-1085)+39]=false
	aN[719] = 2194
	aI = function(...)
	aN[95] = getfenv
	aN[217] = string
	aN[169] = string.char
	mU = true
	aN[106] = "format"
	aN[15] = string[aN[106]]
	local dN
	aN[526][4][1] = aU[1]
	dN = nil
	cg = ck[1]
	ck[1] = nil
	dN = {178, 152, 1, 105, 33}
	cj[1] = nil
	ci = {178, 152, 1, 105, 33}
	mU = true
	ch = {1254137, 755707, 245, 85, 253}
	ci = {242, 52, 100, 195, 200}
	aX[1] = ""
	ck[1] = 1
	cf = 1397988
	local dN
	aN[526][1][1] = cg
	cg = aN[526][4][1]
	dN = aV[1]
	aV[1] = nil
	cj[1] = 1397988
	cf = dN
	mU = true
	aX[1] = "delay"
	bA = "delay"
	local dN
	dN = 12872556
	aW[1] = cg
	cg = {242, 52, 100, 195, 200}
	ci = 12872556
	mU = true
	cj[1] = 2971331
	cg = {156, 242, 14, 228}
	ck[1] = 1
	ch = {2044081, 229797, 229, 221, 139}
	aX[1] = ""
	local dN
	dN = aN[526][1][1]
	aN[526][1][1] = 1
	ck[1] = dN
	mU = true
	aX[1] = "task"
	bR = "task"
	mU = true
	aV[1] = getfenv[bR]
	ci = "delay"
	cm[1] = "delay"
	cg = aV[1][cm[1]]
	aW[1] = 12
	ck[1] = function(...)return(function(...)
	-- for-dispatch over ji=987..851 step -4
	aN = {}
	aN[752] = 9610
	aN[979-294]=979~=907
	aH = 1789
	aN[640] = 5701
	aM = true
	aN[963-134]=963+158
	aN[(959-959)+632]=959+7914
	aN[(875+22)-22]=955~=967
	aN[(951-951)+674]=951+3301
	aN[(947-947)+813]=947~=883
	aN[737] = true
	aN[(659+173)-173]=939+5402
	aN[(935-935)+770]=935+2480
	aN[931-222]=931+3457
	aN[(927-927)+212]=false
	aN[(137+61)-61]=118681
	aN[802] = 8573
	aN[(915-915)+854]=915+8964
	aN[(719+254)-254]=911~=863
	aN[907-52]=907~=895
	aN[(903-903)+850]=903~=939
	aN[899-86]=899+4255
	aN[(895-895)+734]=895~=979
	aN[891-885]=891==891
	aN[(696+412)-412]=887+4396
	aN[(883-883)+686]=883~=891
	aN[(691+10)-10]=879+3205
	aN[875-161]=875+3052
	aN[871-45]=871+3297
	aN[687] = 8554
	aN[863-167]=863~=931
	aI = function(...)local aU,aV,aW=nil,{},{}local ck,cl,cm,cn,co,cp,cq,cr,cs,ct,cu,cx,cC,dC,dE,dG,dJ,dL,cA,fr,fs=...local cj=936794 local mV=true local aX,aY,cf,cg,ch,ci=703378+cj,cj+80106,1821380+cj,cj+69633,(cj-755)+(703378+755),cj+1821380 while true do if(aX-cj)~=703379 then if not((aY-cj)~=80106)then if aN[137]==118681 then aW[1]=aN[137]==118681;aU=aW[1];aV[1]=not aU;cj=cj+10504;if not aV[1]then cj=2629+cj;do local dN;dN=aU;aU=aW[1];aW[1]=dN;end;mV=true;aX,aY=(cj-39)+(703378+39),cj+78414;ch=aX;else cj=cj+397;do local dN;dN=aW[1];aW[1]=aU;aU=dN;end;mV=true;aX,aY=(cj-694)+(703378+694),cj+80415;ch=aX;end;else aN[1031]=aN[137];end;elseif not(78414~=(aY-cj))then while aN[212]do aN[1014]=aN[137];end;cj=2051+cj;aU,aW[1]=aW[1],aU;mV=true;aX,aY=(cj-592)+(703378+592),39343+cj;ch=aX;elseif(aY-cj)==39343 then cj=cj+8220;mV=true;aX=(cj-347)+(703378+347);aY=cj+80106;ch=aX;elseif 80415==(aY-cj)then cj=cj+7399;return;end end end end
	aQ = aI
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @3085
	)(cu,cx,cC,dC,dE,dG,dJ,dL,cA,fr,fs,ft,fF,fG,fH,fI,fJ,fK,fD,fu,fv,...)end
	cl[1] = cg(aW[1],ck[1])
	return
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @5682
	aX = aI
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @7887
	return mS(dE,dG,dJ,dL,cA,fr,fs,ft,fF,fG,cl,fH,fI,fJ,fK,fD,fu,fv,fw,fx,fy,...)end
	local dN
	dN = 12872556
	aN[478][4][1] = nil
	aY = "pcall"
	cj[1] = {178, 152, 1, 105, 33}
	aW[1] = 12872556
	mQ = true
	while aN[144]do aN[1048]=aN[67];end
	local mW=(if not aN[203]then aN[483]else cm[1])
	ck[1] = mW(cg[1])
	cm[1] = getfenv[bK]
	cg[1] = function(...)local mX=function(...)
	-- for-dispatch over mY=253..485 step 8
	aH = 1
	aH = 1
	aN = {}
	aH = 734
	aN[285+580]=285+824
	aM = true
	aN[(301-301)+85]=81995
	aN[309+343]=309+4313
	aN[(317-317)+715]=317~=261
	aN[(621+341)-341]=325~=461
	aN[333+439]=333+3784
	aN[341-286]=true
	aN[(349-349)+815]=349+2094
	aN[774] = 8186
	aN[365+381]=365+829
	aN[750] = 6989
	aN[(389-389)+73]=not true
	aN[864] = 4749
	aN[405+364]=405+5999
	aN[651] = 7292
	aN[421+235]=421+3359
	aN[(897+36)-36]=437+4322
	aN[445+194]=445+6021
	aN[(762+407)-407]=453+6778
	aN[(833+319)-319]=461~=341
	aY = function(...)
	aN[217] = getfenv
	aN[11] = string
	aN[100] = string.char
	local dN
	dN = {178, 152, 1, 105, 33}
	cj[1] = nil
	ck = 12872556
	aW[1] = {178, 152, 1, 105, 33}
	ni = true
	cm,cn=(cs-713)+(1714316+713),33758+cs
	repeat if bR==nil then cj[1]='';aV[1]={226,198,141,(120-14)+14};aX[1]={((cs+3577714)-(cs+638405)),((cs+2481211)-(cs+163020)),((cs+796372)-(cs+796315)),((cs+132145)-(cs+132026)),((cs+235827)-(cs+235614))};aN[419][4][1]=((cs+11364977)-(cs+708807));ci=1;end;cs=5944+cs;cs=(2240+cs);do local dN;dN=aX[1];aX[1]=cj[1];cj[1]=dN;dN=ch[1];ch[1]=aU[1];aU[1]=dN;dN=cf;cf=ci;ci=dN;end;ni=true;cm=132845+cs;cn=(cs-646)+(76977+646);cq=cm;until aN[55]
	aX[1] = bZ(aV[1],cj[1],aN[419][4][1])
	bR = aX[1]
	ni = true
	cm,cn=1679005+cs,cs+25849
	aN[419][1][1] = getfenv[bR]
	ch[1] = nil
	local dN
	dN = nil
	aY = true
	aV[1] = nil
	ni = true
	cm,cn=(cs-153)+(1679005+153),cs+82414
	aN[946] = 632367
	ck = nil
	aY = aN[419][1][1][ck]
	aW[1] = function(...)local nj=function(...)
	-- for-dispatch over nk=255..441 step 6
	aH = 1
	aN = {}
	aN[(814+506)-506]=267+3135
	aN[623] = 5275
	aH = 557
	aM = true
	aN[(690+90)-90]=291+4969
	aN[(833+243)-243]=297+9236
	aN[303+305]=303+8187
	aN[879] = 3584
	aN[315+432]=315+5276
	aN[638] = 6931
	aN[(151+373)-373]=251366
	aN[(811+171)-171]=333~=273
	aN[339+479]=339+8106
	aN[822] = 5470
	aN[(351-351)+807]=351+5687
	aN[(357-357)+696]=357+3070
	aN[363+428]=363+4053
	aN[369+420]=369+6883
	aN[375+430]=375+5350
	aN[(614+335)-335]=381+3702
	aN[627] = 5794
	aN[393+279]=393+5771
	aN[(399-399)+65]=not true
	aN[405+446]=405+9132
	aN[(411-411)+112]=not false
	aN[417+342]=417+1621
	aN[423+400]=423+2560
	aH = function(...)
	aN[38] = getfenv
	aN[135] = string
	aN[76] = string.char
	mJ = true
	aN[19] = "format"
	aN[150] = string[aN[19]]
	local dN
	dN = 1
	cn[1] = nil
	cr = {186, 98, 48, 9, 184}
	aV[1] = 1
	mJ = true
	cs = ""
	cr = 1
	ci[1] = 7557569
	ck[1] = {2713365, 1052361, 133, 163, 1}
	cg[1] = {115, 33, 28, 57}
	mJ = true
	cs = "wait"
	fp = "wait"
	local dN
	aW[1] = nil
	aN[337][3][1] = co[1]
	dN = "wait"
	cs = aN[337][2][1]
	aN[337][2][1] = "wait"
	mJ = true
	if bK==nil then
	ck[1] = {1833181, 3498327, 121, 61, 1}
	cr = 1
	ci[1] = 14229552
	ch = {22, 150, 30, 120, 127}
	aN[337][2][1] = ""
	end
	local dN
	aY[1] = nil
	aW[1] = nil
	dN = nil
	cg[1] = cC
	cC = nil
	dN = cs
	cs = "spawn"
	cl[1] = dN
	mJ = true
	aN[922] = aN[151]+201
	if bK==nil then
	aN[337][2][1] = cc(ch,ck[1],ci[1])
	bK = "wait"
	end
	mJ = true
	if bR==nil then
	ci[1] = 14230648
	aN[337][2][1] = ""
	cl[1] = 1
	ck[1] = {1902125, 1757689, 153, 131, 187}
	ch = {105, 165, 108, 90}
	end
	local dN
	cu[1] = nil
	dN = {2713365, 1052361, 133, 163, 1}
	ck[1] = cp[1]
	cp[1] = {2713365, 1052361, 133, 163, 1}
	dN = {2331465, 1754225, 115, 181, 19}
	aX[1] = cg[1]
	cg[1] = {2331465, 1754225, 115, 181, 19}
	mJ = true
	if bR==nil then
	aN[337][2][1] = bZ(ch,cp[1],ci[1])
	bR = "wait"
	end
	local dN
	aW[1] = aN[337][3][1]
	dN = aX[1]
	aX[1] = {79, 251, 6, 169, 61, 135}
	cf[1] = dN
	dN = 1
	aV[1] = true
	cq[1] = 1
	mJ = true
	aX[1] = 1
	co[1] = 1
	co[1] = 1
	cC = 1
	mJ = true
	cr = 1
	local dN
	dN = "wait"
	aN[337][2][1] = nil
	cf[1] = "wait"
	mJ = true
	ct = 0
	cg[1] = true
	aN[337][4][1] = true
	aW[1] = false
	cn[1] = false
	aY[1] = true
	cu[1] = false
	aN[337][2][1] = true
	local dN
	dN = "wait"
	cf[1] = false
	aW[1] = "wait"
	mJ = true
	mJ = true
	cm[1] = 1
	cj[1] = getfenv[bK]
	cg[1] = function(...)local jD=function(...)
	-- for-dispatch over iW=301..361 step 2
	aN = {}
	aN[303+542]=303+1989
	aN[(305-305)+774]=305+2909
	aH = 545
	aM = true
	aN[(311-311)+684]=311+1515
	aN[313+397]=313+8049
	aN[(803+385)-385]=315~=301
	aN[(317-317)+608]=317+7621
	aN[613] = 4336
	aN[24] = 729487
	aN[621] = 5738
	aN[(693+281)-281]=325+1969
	aN[(806+58)-58]=327~=345
	aN[329+311]=329+8468
	aN[639] = 1921
	aN[333+360]=333~=357
	aN[335+431]=335+8022
	aN[(858+272)-272]=337+5177
	aN[(339-339)+660]=339+2058
	aN[(693+224)-224]=341~=351
	aN[343+462]=343+7829
	aN[345+300]=345~=327
	aN[(42+138)-138]=347==347
	aN[(349-349)+108]=349~=349
	aN[(351-351)+683]=351+1410
	aN[745] = 7549
	aN[(823+304)-304]=355+6624
	aW = function(...)
	aN[150] = getfenv
	aN[146] = string
	aN[41] = string.char
	kY = true
	ct,cu=(dG-523)+(1442129+523),(dG-816)+(98959+816)
	cr[1] = cb(cj[1],aN[337][3][1],aN[337][1][1])
	nu = cr[1]
	local dN
	dN = nil
	cs[1] = {2713365, 1052361, 133, 163, 1}
	cp[1] = nil
	kY = true
	cu = 883920
	aN[974] = 729864
	cr[1] = ""
	aV[1] = 1
	cj[1] = {23, 128, 164, 196, 99, 236, 248, 115, 78, 59, 92}
	aN[337][3][1] = {1056657, 537607, 69, 145, 105}
	aN[337][1][1] = 4502534
	local dN
	dN = 1
	aV[1] = 4502534
	aN[337][1][1] = 1
	dN = aN[337][4][1]
	aN[337][4][1] = {1056657, 537607, 69, 145, 105}
	aN[337][3][1] = dN
	kY = true
	cu = 826955
	aN[337][1][1] = bZ(cs[1],cn,cm)
	nr = aN[337][1][1]
	kY = true
	cu = 900225
	repeat if nt==nil then cm=((dG+5913806)-(dG+483698));aN[337][1][1]='';cr[1]={50,136,58,48};aN[337][2][1]=1;cn={((dG+4055841)-(dG+341624)),((dG+2436561)-(dG+757208)),((dG+530950)-(dG+530695)),((dG+69721)-(dG+69502)),((dG+775628)-(dG+775583))};end;dG=(709+dG);dG=(2258+dG);cn,ci[1],aN[337][2][1],aN[337][1][1],ch[1],aV[1],cr[1]=ch[1],co[1],aV[1],cr[1],cn,aN[337][2][1],aN[337][1][1];kY=true;ct=(dG-220)+(664065+220);cu=dG+44217;dC=ct;until aN[42]
	cr[1] = cc(aN[337][1][1],ch[1],cm)
	nt = cr[1]
	kY = true
	cu = 865640
	aN[983] = 730133
	aN[337][1][1] = ce(cj[1],aN[337][4][1],aN[337][3][1])
	nq = aN[337][1][1]
	local dN
	aW = nil
	aN[337][2][1] = cr[1]
	cr[1] = {23, 128, 164, 196, 99, 236, 248, 115, 78, 59, 92}
	dN = 1
	co[1] = 7557569
	cg = 1
	kY = true
	ct,cu=dG+1894823,dG+98718
	aN[337][1][1] = ""
	aN[337][2][1] = 1
	cj[1] = {168, 71, 121, 220, 229, 183, 223, 135, 244, 132}
	aN[337][4][1] = {3465201, 2078717, 147, 119, 9}
	cr[1] = 3153234
	local dN
	dN = nil
	ci[1] = {3465201, 2078717, 147, 119, 9}
	aN[337][4][1] = nil
	dN = 1
	aX[1] = 1
	aN[337][2][1] = 1
	dN = 1
	cg = 48
	aY[1] = 1
	kY = true
	cu = 917002
	if nu==nil then
	aN[337][1][1] = {136, 122, 135, 1, 62, 43, 248, 107, 55, 7}
	ci[1] = 10416199
	cr[1] = ""
	ch[1] = {248745, 2052291, 113, 197, 193}
	aV[1] = 1
	end
	kY = true
	cu = 865405
	cr[1] = cc(cj[1],aN[337][4][1],aV[1])
	no = cr[1]
	kY = true
	cu = 891196
	if nq==nil then
	aN[337][1][1] = ""
	cr[1] = 1
	aN[337][4][1] = {305397, 2894485, 27, 235, 217}
	aN[337][3][1] = 6087623
	cj[1] = {183, 186, 229, 117, 89, 171, 140, 83, 223, 81, 30}
	end
	kY = true
	cu = 883741
	aN[70] = "format"
	aN[203] = string[aN[70]]
	kY = true
	ct,cu=(dG-477)+(1442129+477),81090+dG
	repeat if nv==nil then co[1]={((dG+950744)-(dG+265331)),((dG+4620284)-(dG+736827)),((dG+659682)-(dG+659457)),((dG+927299)-(dG+927142)),((dG+225153)-(dG+225082))};cf={191,96,232,24,(35+5)-5,248,220,(73-8)+8,241,(184-5)+5,102,205,(228+4)-4};ck[1]='';cm=((dG+15517471)-(dG+918099));cg=1;end;dG=(6068+dG);dG=(9904+dG);cs[1],cj[1],aV[1],ck[1],aN[337][2][1],aN[337][1][1]=aN[337][1][1],aV[1],cj[1],cs[1],cg,ck[1];kY=true;ct,cu=dG+1442129,(dG-643)+(42438+643);dC=ct;until aN[42]
	aN[337][1][1] = bZ(cf,co[1],cm)
	nv = aN[337][1][1]
	aX[1] = nil
	kY = true
	cu = 934577
	aN[337][2][1] = 1
	cm = 2405560
	aN[337][1][1] = ""
	aX[1] = {241, 207, 31, 198, 169, 130, 211}
	co[1] = {3843521, 3448085, 171, 71, 23}
	local dN
	aN[337][4][1] = nil
	aU = ""
	cr[1] = ""
	dN = 1
	aY[1] = nil
	aV[1] = nil
	ck[1] = 1
	kY = true
	ct,cu=dG+198703,(dG-873)+(3880+873)
	aN[337][1][1] = ce(cj[1],ci[1],cr[1])
	nm = aN[337][1][1]
	local dN
	cp[1] = ""
	aU = {3465201, 2078717, 147, 119, 9}
	dN = {3843521, 3448085, 171, 71, 23}
	co[1] = nil
	aN[337][4][1] = {3843521, 3448085, 171, 71, 23}
	kY = true
	cu = 935207
	aU = {127, 55, 236, 240, 11, 111, 114, 74, 24, 36}
	aN[337][1][1] = ""
	aX[1] = 1
	ci[1] = {1393289, 2145131, 143, 25, 37}
	cr[1] = 698921
	kY = true
	cu = 1011745
	aN[337][1][1] = "ErrorTitle"
	np = "ErrorTitle"
	kY = true
	ct,cu=1476106+dG,dG+30580
	if no==nil then
	cr[1] = cc(cj[1],aN[337][4][1],aV[1])
	no = cr[1]
	end
	local dN
	ci[1] = nil
	co[1] = {3843521, 3448085, 171, 71, 23}
	dN = "ErrorTitle"
	cp[1] = ""
	cq[1] = "ErrorTitle"
	dN = nil
	aV[1] = 4502534
	aN[337][3][1] = nil
	dN = 7557569
	aN[337][1][1] = 698921
	cr[1] = 7557569
	kY = true
	cu = 978045
	repeat if nq==nil then aN[337][3][1]=((dG+6769363)-(dG+681740));cj[1]={183,186,229,117,89,171,(140-25)+25,83,223,81,30};aN[337][4][1]={((dG+369714)-(dG+64317)),((dG+3809067)-(dG+914582)),((dG+560941)-(dG+560914)),((dG+347782)-(dG+347547)),((dG+371302)-(dG+371085))};cr[1]=1;aN[337][1][1]='';end;dG=dG+7631;dG=(dG+4765);cm,ck[1],cq[1],ci[1]=cq[1],ci[1],cm,aN[337][2][1];kY=true;ct,cu=(dG-712)+(1894823+712),5337+dG;dC=ct;until aN[42]
	aN[337][1][1] = cb(aX[1],co[1],cm)
	nl = aN[337][1][1]
	local dN
	dN = {23, 128, 164, 196, 99, 236, 248, 115, 78, 59, 92}
	cs[1] = 1
	aX[1] = {23, 128, 164, 196, 99, 236, 248, 115, 78, 59, 92}
	kY = true
	ct,cu=(dG-453)+(198703+453),dG+31047
	if nr==nil then
	cm = 8546436
	cs[1] = {88, 110, 251, 171, 58, 167, 235, 57, 126, 123, 80, 36, 101, 20, 6}
	aN[337][2][1] = 1
	co[1] = {3870829, 1205943, 115, 19, 201}
	aN[337][1][1] = ""
	end
	kY = true
	cu = 1058678
	cp[1] = cb(co[1],ci[1],cr[1])
	nn = cp[1]
	kY = true
	ct,cu=546955+dG,(dG-918)+(2953+918)
	cl[1] = {3182401, 3220329, 3, 21, 73}
	aW = ""
	co[1] = {135, 227, 107, 179, 82, 8, 175, 139, 48, 230}
	cs[1] = 1
	cr[1] = 10236573
	kY = true
	ct,cu=546955+dG,dG+70473
	aW = "GetService"
	bf = "GetService"
	local dN
	cq[1] = 1
	dN = 1
	cr[1] = 1
	cp[1] = nil
	aU = 1
	kY = true
	ct,cu=546955+dG,62704+dG
	cl[1] = {3189317, 1346755, 237, 107, 137}
	cs[1] = 1
	aW = ""
	co[1] = {64, 152, 136, 172, 16, 246, 82, 191, 131, 102, 215, 230, 166}
	ch[1] = 6133832
	kY = true
	cu = 1096846
	aW = "Session ended"
	ns = "Session ended"
	local dN
	aN[337][3][1] = aY[1]
	dN = {23, 128, 164, 196, 99, 236, 248, 115, 78, 59, 92}
	cf = 1
	aN[337][4][1] = {23, 128, 164, 196, 99, 236, 248, 115, 78, 59, 92}
	dN = 1
	cr[1] = 2405560
	cm = 1
	dN = 1
	cs[1] = 4502534
	aV[1] = 1
	kY = true
	cu = 1098061
	cq[1] = fG[1]
	aN[337][2][1] = "GetService"
	cn = "GetService"
	ci[1] = cq[1][cn]
	aU = nl
	kY = true
	ct,cu=dG+489339,97400+dG
	cn = ci[1](cq[1],aU)
	cp[1] = nr
	cj[1] = cn[cp[1]]
	cs[1] = nv
	cr[1] = cj[1][cs[1]]
	ck[1] = no
	aN[337][3][1] = cr[1][ck[1]]
	aN[337][4][1] = aN[337][3][1]
	local dN
	dN = ci[1]
	ci[1] = {64, 152, 136, 172, 16, 246, 82, 191, 131, 102, 215, 230, 166}
	co[1] = dN
	kY = true
	ct,cu=(dG-361)+(489339+361),74262+dG
	aN[337][2][1] = "Session ended"
	cm = "Session ended"
	cq[1] = "Session ended"
	co[1] = nu
	aU = aN[337][4][1][co[1]]
	cn = "ErrorTitle"
	cp[1] = aU[cn]
	cj[1] = nt
	cp[1][cj[1]]=cq[1]
	local dN
	aY[1] = aU
	aX[1] = "Session ended"
	cm = {3189317, 1346755, 237, 107, 137}
	dN = "Session ended"
	aW = aN[337][4][1]
	aN[337][4][1] = "Session ended"
	dN = aN[337][3][1]
	aN[337][3][1] = cp[1]
	cp[1] = dN
	dN = co[1]
	co[1] = ck[1]
	ck[1] = dN
	kY = true
	ct,cu=(dG-161)+(489339+161),(dG-23)+(31436+23)
	aX[1] = fK[1]
	cq[1] = aX[1]
	ck[1] = nq
	aY[1] = aW[ck[1]]
	cn = nm
	aN[337][3][1] = aY[1][cn]
	cj[1] = nn
	cs[1] = aN[337][3][1][cj[1]]
	cr[1] = nt
	cs[1][cr[1]]=cq[1]
	return
	aN[1002] = 729491
	if nn==nil then
	cr[1] = 12527230
	ci[1] = {3701917, 2390687, 93, 209, 225}
	cj[1] = 1
	cp[1] = ""
	aU = {255, 156, 172, 140, 34, 210, 131, 219, 19, 231, 68, 62}
	end
	kY = true
	ct,cu=(dG-818)+(546955+818),53067+dG
	if nu==nil then
	ch[1] = {248745, 2052291, 113, 197, 193}
	ci[1] = 10416199
	aV[1] = 1
	aN[337][1][1] = {136, 122, 135, 1, 62, 43, 248, 107, 55, 7}
	cr[1] = ""
	end
	kY = true
	cu = 1239771
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @13142
	aV = aW
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @15067
	return jD(cm,fs,ft,fF,fG,fH,fI,fJ,fK,fD,fu,fv,fw,fx,fy,fz,fA,fB,fC,fP,fQ,fR,...)end
	aN[337][4][1] = cj[1](cg[1])
	cj[1] = getfenv[bR]
	cs = "wait"
	cg[1] = "wait"
	aN[337][4][1] = cj[1][cg[1]]
	aN[337][2][1] = 0.25
	cn[1] = aN[337][4][1](aN[337][2][1])
	cj[1] = 2
	cp[1] = 2
	local dN
	ci[1] = 7557569
	ct = 2
	dN = aN[337][2][1]
	aN[337][2][1] = true
	co[1] = 1
	cf[1] = "wait"
	aW[1] = dN
	dN = {2713365, 1052361, 133, 163, 1}
	aN[337][3][1] = 2
	cp[1] = {2713365, 1052361, 133, 163, 1}
	dN = nil
	cq[1] = 48
	ch = {115, 33, 28, 57}
	aY[1] = true
	aU = nil
	mJ = true
	return
	local dN
	cx[1] = 48
	ct = 1
	cC = 7557569
	dN = true
	aY[1] = {115, 33, 28, 57}
	ch = 48
	cq[1] = false
	cu[1] = nil
	aU = true
	dN = "wait"
	cf[1] = true
	aN[337][2][1] = "wait"
	mJ = true
	-- region end
	-- warn: repeat-until 'aN[112]' not pre-true; one-shot assumed
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @20861
	aY = aH
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @22852
	return nj(ct,cu,cx,cC,dC,dE,dG,dJ,dL,cA,fr,fs,ft,fF,fG,fH,fI,fJ,fK,fD,fu,...)end
	ci = aY(aW[1])
	return
	aN[23] = "format"
	aN[14] = string[aN[23]]
	local dN
	dN = nil
	cf = nil
	cl = nil
	dN = nil
	ch[1] = aW[1]
	aW[1] = nil
	dN = nil
	ck = aU[1]
	aU[1] = nil
	ni = true
	cm,cn=1355358+cs,(cs-515)+(52849+515)
	aX[1] = 1
	aY = ""
	aW[1] = {2331465, 1754225, 115, 181, 19}
	aV[1] = {186, 98, 48, 9, 184}
	cl = 7305910
	local dN
	dN = ci
	ci = nil
	aU[1] = dN
	dN = nil
	cj[1] = ""
	aY = nil
	ni = true
	cm,cn=1355358+cs,(cs-204)+(47688+204)
	cj[1] = "spawn"
	fk = "spawn"
	ni = true
	cm = 428013
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @25949
	aL = aY
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @27776
	return mX(dE,dG,dJ,dL,cA,fr,fs,ft,fF,fG,cl,fH,fI,fJ,fK,fD,fu,fv,fw,fx,fy,...)end
	local nw=(if not aN[144]then cm[1]else aN[504])
	ck[1] = nw(cg[1])
	cm[1] = getfenv[bK]
	cg[1] = function(...)local mO=function(...)
	-- for-dispatch over fX=898..1038 step 5
	aN = {}
	aN[(612+268)-268]=903+6673
	aH = 1694
	aN[(780+17)-17]=913~=968
	aN[680] = true
	aM = true
	aN[758] = 8256
	aN[933-70]=933+5038
	aN[938-109]=938+6153
	aN[943-98]=943+7668
	aN[953-247]=953+4358
	aN[963-255]=963+2395
	aN[968-203]=968+2705
	aN[(876+268)-268]=973+7396
	aN[(98+250)-250]=537388
	aN[(874+258)-258]=983+9542
	aN[(988-988)+605]=988+4419
	aN[993-163]=993+2377
	aN[998-911]=not false
	aN[856] = true
	aN[(738+123)-123]=1008~=963
	aN[1013-284]=1013~=983
	aN[1018-226]=1018~=968
	aN[(157+29)-29]=not true
	aI = function(...)
	aN[29] = getfenv
	aN[192] = string
	aN[138] = string.char
	mr = true
	while aN[157]do aN[1003]=aN[98];end
	aN[213] = "format"
	aN[108] = string[aN[213]]
	mr = true
	while aN[157]do aN[980]=aN[98];end
	cl = ""
	ch[1] = {578789, 2874553, 251, 81, 37}
	aU = {190, 53, 113, 194, 27, 206, 181, 215, 55, 97}
	ck = 8506129
	aV = 1
	mr = true
	repeat ci[1]=cj[1][cm[1]];aX=bm;cg=ci[1](cj[1],aX);aW=bk;cf=cg[aW];dE=dE+19939;dE=(6004+dE);do local dN;cl=cm[1];cp[1]=ch[1];ch[1]=aY[1];aY[1]=cr[1];dN=ci[1];ci[1]=cg;cg=dN;end;mr=true;cs,ct=(dE-962)+(634238+962),dE+44038;cC=cs;until aN[87]
	aN[377][2][1] = nil
	aN[377][3][1] = nil
	aV = cf[aN[377][3][1]]
	cq[1] = fI[1]
	ch[1] = aV(cf,cq[1])
	return
	cl = "GetService"
	bf = "GetService"
	local dN
	dN = cq[1]
	cq[1] = nil
	cn[1] = dN
	mr = true
	cl = ""
	ck = 928234
	aV = 1
	cj[1] = {100, 125, 115, 3, 191, 232, 99}
	cr[1] = {700721, 990601, 243, 95, 153}
	mr = true
	cl = "Players"
	bm = "Players"
	local dN
	aN[377][4][1] = nil
	cg = cn[1]
	cf = nil
	dN = {100, 125, 115, 3, 191, 232, 99}
	cj[1] = {700721, 990601, 243, 95, 153}
	cr[1] = {100, 125, 115, 3, 191, 232, 99}
	mr = true
	ck = 111908
	cl = ""
	cr[1] = {216, 4, 155, 193, 107, 219, 42, 210, 77, 102, 199}
	aV = 1
	cj[1] = {3169189, 975163, 237, 173, 107}
	local dN
	cn[1] = {216, 4, 155, 193, 107, 219, 42, 210, 77, 102, 199}
	dN = {3169189, 975163, 237, 173, 107}
	cj[1] = 1
	aX = {3169189, 975163, 237, 173, 107}
	dN = nil
	aW = {178, 152, 1, 105, 33}
	aU = nil
	mr = true
	cl = "LocalPlayer"
	bk = "LocalPlayer"
	local dN
	dN = nil
	co[1] = 1
	aV = nil
	dN = cq[1]
	cq[1] = aY[1]
	aY[1] = dN
	mr = true
	cl = ""
	ck = 4412573
	cn[1] = {92, 175, 134, 143}
	co[1] = 1
	aX = {3242749, 342735, 173, 225, 229}
	local dN
	aN[377][2][1] = nil
	ci[1] = nil
	aN[377][4][1] = {3242749, 342735, 173, 225, 229}
	aX = nil
	dN = nil
	aV = nil
	aN[377][3][1] = nil
	mr = true
	cl = "Kick"
	bi = "Kick"
	local dN
	dN = nil
	aV = cg
	cg = nil
	dN = ch[1]
	ch[1] = cq[1]
	cq[1] = dN
	mr = true
	cj[1] = ft[1]
	cm[1] = "GetService"
	local dN
	cr[1] = "Kick"
	dN = nil
	ci[1] = {178, 152, 1, 105, 33}
	aW = nil
	cf = nil
	mr = true
	if bf==nil then
	cl = cb(cj[1],cr[1],ck)
	bf = "Kick"
	end
	local dN
	dN = cq[1]
	cq[1] = {92, 175, 134, 143}
	cn[1] = dN
	mr = true
	if bm==nil then
	cr[1] = {700721, 990601, 243, 95, 153}
	ck = 928234
	cj[1] = {100, 125, 115, 3, 191, 232, 99}
	cl = ""
	aV = 1
	end
	mr = true
	if aN[98]==537388 then
	if bm==nil then cl=cc(cj[1],cr[1],ck);bm=cl;end
	dE = 513075
	dE = 519511
	do local dN;aN[377][4][1]=cg;cg=cn[1];cf=ci[1];dN=cr[1];cr[1]=cj[1];cj[1]=dN;end
	mr = true
	cs = 2048863
	ct = 596620
	cC = 1643044
	else
	aN[967] = nil
	end
	if bk==nil then
	aV = 1
	cl = ""
	ck = 111908
	cj[1] = {3169189, 975163, 237, 173, 107}
	cr[1] = {216, 4, 155, 193, 107, 219, 42, 210, 77, 102, 199}
	end
	local dN
	cn[1] = "Kick"
	dN = cj[1]
	cj[1] = nil
	aX = dN
	dN = nil
	aU = {92, 175, 134, 143}
	aW = nil
	mr = true
	-- region end
	-- warn: no leaf for key (1536836, 54723)
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @5901
	aK = aI
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @7786
	return mO(dE,dG,dJ,dL,cA,fr,fs,ft,fF,fG,cl,fH,fI,fJ,fK,fD,fu,fv,fw,fx,fy,...)end
	ck[1] = cm[1](cg[1])
	local dN
	ch = cq[1]
	cq[1] = 200
	mQ = true
	cq[1] = true
	aU[1] = true
	cm[1] = true
	aN[478][4][1] = false
	mQ = true
	cm[1] = nil
	cm[1] = (if not aN[144]then getfenv[by]else aN[526])
	cg[1] = nil
	cg[1] = "yield"
	aN[478][1][1] = cm[1][cg[1]]
	cp[1] = aN[478][1][1]()
	mQ = true
	local dN
	dN = cg[1]
	cg[1] = "yield"
	cm[1] = dN
	dN = 1
	ck[1] = aY
	aY = "pcall"
	aN[478][1][1] = 1
	mQ = true
	aN[1046] = 231357
	return
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @50758
	aS = aL
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @53099
	return mO(aN[534][11],fu,fv,aN[534][14],aN[534][6],aW,fw,aN[534][4],aX,dJ,aY,fx,aN[534][18],aN[534][12],cu,dC,aN[534][9],co,cC,cx,...)end
	fD = 270817
	aU[1] = nil
	fD = 271877
	aN[534][6][1] = "Wait"
	fD = 272518
	ck[1] = function(...)local jD=function(...)
	-- for-dispatch over ga=847..1078 step 7
	aH = 1
	aN = {}
	aH = 1146
	aN[(868-868)+865]=868+3339
	aN[875-100]=875~=987
	aM = true
	aN[889-676]=754651
	aN[(45+21)-21]=true
	aN[702] = 1792
	aN[910-251]=910+2283
	aN[(810+205)-205]=917+734
	aN[(924-924)+698]=924+1067
	aN[778] = 7665
	aN[(801+440)-440]=938+4671
	aN[(702+68)-68]=945+1992
	aN[952-142]=952+5326
	aN[959-253]=959~=966
	aN[973-352]=973+4989
	aN[603] = true
	aN[(704+483)-483]=987~=917
	aN[(727+431)-431]=994+2652
	aN[1001-366]=1001+9812
	aN[1008-332]=1008+4736
	aN[(1015-1015)+641]=1015+694
	aN[(846+108)-108]=1022~=854
	aN[(756+351)-351]=1029+1150
	aN[837] = 1610
	aN[(613+340)-340]=1043+3056
	aN[96] = false
	aN[(1057-1057)+894]=1057+8165
	aK = function(...)
	cn[1] = fY
	cg[1] = fZ
	cx[1] = fO
	while aN[96]do aN[959]=aN[213];end
	cm = bZ(cC[1],aY[1],aN[424][4][1])
	fk = cm
	nx = true
	nx = true
	local dN
	aN[424][3][1] = nil
	cs[1] = nil
	aN[424][4][1] = nil
	aN[424][2][1] = nil
	cC[1] = nil
	ci = nil
	co = 1
	cl[1] = nil
	ct[1] = nil
	ck = nil
	dL = nil
	cf = nil
	dC[1] = nil
	dN = nil
	aN[424][1][1] = nil
	cu = nil
	dN = aY[1]
	aY[1] = "Wait"
	aU[1] = dN
	dN = nil
	dJ[1] = nil
	dG = nil
	cr = nil
	nx = true
	aN[990] = aN[213]+745
	dC[1] = getfenv[bR]
	cC[1] = (if aN[213]==754651 then aN else aN[467])
	cC[1] = nil
	ch[1] = nil
	dL = dC[1][(if aN[213]~=754651 then aN[449]else ch[1])]
	cr = (if aN[45]then dL else aN[436])()
	dC[1] = getfenv[fo]
	aV = nil
	aU[1] = nil
	ck = dE[1][(if not aN[96]then aU[1]else aN[427])]
	cj[1] = (if aN[45]then dC[1]else aN)(ck)
	cr = cj[1]
	local dN
	cs[1] = nil
	aW = nil
	cl[1] = ck
	cC[1] = 1
	dN = nil
	aV = nil
	aN[424][2][1] = nil
	dN = cr
	cr = dC[1]
	dC[1] = dN
	nx = true
	aN[1009] = aN[213]+473
	cq[1] = dC[1]
	aW = cq[1]
	ct[1] = aW
	cu = not cq[1]
	local nz=cu
	nx = true
	nx = true
	nx = true
	ci = nil
	local nA,gO=dE[1],ci
	dJ[1] = nA[gO]
	ct[1] = nil
	ct[1] = nil
	local dN
	aN[424][3][1] = cl[1]
	ck = nil
	dC[1] = nil
	nx = true
	cl[1] = 1
	cm = ""
	cs[1] = {102, 207, 40, 0}
	aY[1] = {519605, 3783995, 131, 61, 237}
	dJ[1] = 13552193
	local dN
	aU[1] = nil
	dN = cC[1]
	cC[1] = {102, 207, 40, 0}
	cs[1] = dN
	dN = "Wait"
	cr = nil
	aN[424][1][1] = "Wait"
	dN = aW
	aW = aN[424][3][1]
	aN[424][3][1] = dN
	nx = true
	cm = "wait"
	fp = "wait"
	local dN
	dN = nil
	aU[1] = nil
	aV = nil
	dN = nil
	aN[424][4][1] = 13552193
	dJ[1] = nil
	nx = true
	if fk==nil then
	aN[424][4][1] = 9974019
	aY[1] = {431193, 622995, 203, 91, 65}
	cm = ""
	cC[1] = {174, 253, 57, 73, 233}
	cl[1] = 1
	end
	local dN
	cj[1] = 1
	dN = aW
	aW = nil
	dJ[1] = dN
	dN = nil
	ch[1] = nil
	ck = nil
	nx = true
	if bV==nil then
	aN[424][2][1] = 3996165
	aN[424][3][1] = {7, 34, 183, 251}
	cm = ""
	cl[1] = 1
	aU[1] = {829085, 521113, 239, 133, 71}
	end
	nx = true
	if bV==nil then
	cm = cb(aN[424][3][1],aU[1],aN[424][2][1])
	bV = "StatusCode"
	end
	nx = true
	repeat if eU==nil then aU[1]={((fI+1714103)-(fI+453314)),((fI+3280261)-(fI+439702)),((fI+778491)-(fI+778446)),((fI+845788)-(fI+845625)),((fI+19879)-(fI+19830))};cm='';aN[424][3][1]={(199-4)+4,237,(224+27)-27,127,79};aN[424][2][1]=((fI+16485782)-(fI+35678));cl[1]=1;end;fI=(3912+fI);fI=(3871+fI);do local dN;dN=co;co=ct[1];ct[1]=dN;dN=aY[1];aY[1]=aU[1];aU[1]=dN;end;nx=true;fr=(fI-320)+(385408+320);fs=(fI-748)+(84977+748);fG=fr;until aN[45]
	aN[424][2][1] = getfenv[fg]
	cr = nil
	nx = true
	local nB,nC=aN[424][2][1],cr
	aW = nB[nC]
	local nD=aW
	ct[1] = nD()
	cC[1] = (if aN[213]~=754651 then aN[473]else dG>ct[1])
	co = cC[1]
	nx = true
	aY[1] = ""
	aU[1] = {3610089, 2726127, 9, 157, 95}
	cm = 8775142
	cs[1] = {13, 67, 134, 232}
	cl[1] = 1
	local dN
	ci = nil
	cr = nil
	dJ[1] = nil
	dN = ""
	aY[1] = 8775142
	cm = ""
	nx = true
	cm = "task"
	bR = "task"
	nx = true
	return "table", ct[1]
	aN[201] = getfenv
	aN[36] = string
	aN[118] = string.char
	local dN
	dN = nil
	cr = 8775142
	aY[1] = nil
	nx = true
	cj[1] = {1, 115, 160, 130, 40}
	cm = 1
	aN[424][4][1] = {2171413, 1558679, 231, 201, 27}
	cl[1] = 10751177
	ci = ""
	nx = true
	aN[1083] = aN[213]+320
	ci = "table"
	fm = "table"
	local dN
	dN = "table"
	ci = nil
	aY[1] = "table"
	dN = "Wait"
	cm = 10751177
	cl[1] = "Wait"
	nx = true
	cj[1] = {85, 121}
	aN[424][4][1] = {3522885, 3185323, 91, 243, 187}
	cm = 11469896
	aN[424][1][1] = 1
	aY[1] = ""
	local dN
	co = nil
	dN = 1
	cq[1] = {3610089, 2726127, 9, 157, 95}
	ch[1] = 1
	dN = 8775142
	cr = nil
	dG = 8775142
	nx = true
	while aN[96]do aN[950]=aN[213];end
	nx = true
	aN[1041] = aN[213]+346
	local nH=cx[1]
	cf = nH()
	nx = true
	dL = aX[1]
	ch[1] = nil
	ch[1] = {}
	local dN
	aW = cs[1]
	dN = aN[424][1][1]
	aN[424][1][1] = nil
	ck = dN
	dN = {3522885, 3185323, 91, 243, 187}
	aN[424][4][1] = 8775142
	cr = {3522885, 3185323, 91, 243, 187}
	nx = true
	dL = {}
	aN[424][1][1] = nil
	aN[424][1][1] = {}
	cm = not ch[1]
	aN[424][4][1] = getfenv[bV]
	local nI=aN[424][4][1]
	dG = nI(dE[1])
	cs[1] = "table"
	aW = (if cs[1]~=dG then not aN[96]else aN[213]~=754651)
	co = (if aN[213]~=754651 then aN[473]else aN[483])
	co = (if not aN[96]then not aW else aN[483])
	ci = (if aN[213]~=754651 then aN[486]else cp)
	nx = true
	while aN[96]do aN[998]=aN[213];end
	cr = cp
	cu = nil
	cu = (if not aN[96]then not ci else aN[438])
	dG = cr+aW
	ct[1] = dG
	local dN
	dN = dG
	dG = ct[1]
	ct[1] = dN
	nx = true
	dC[1] = true
	co = true
	dJ[1] = false
	local nJ=dJ[1]
	nx = true
	aY[1] = cc(cj[1],aN[424][4][1],cm)
	fg = aY[1]
	local dN
	dN = aV
	aV = 1
	cf = dN
	nx = true
	cm = 1445385
	aY[1] = ""
	cj[1] = {208, 62, 30, 14}
	aN[424][4][1] = {769601, 610449, 199, 15, 31}
	aN[424][1][1] = 1
	nx = true
	aY[1] = "Body"
	eE = "Body"
	local dN
	aU[1] = {769601, 610449, 199, 15, 31}
	cs[1] = cr
	cr = "table"
	aN[424][2][1] = {208, 62, 30, 14}
	dN = ci
	ci = cu
	cu = dN
	nx = true
	aN[424][1][1] = 1
	aN[424][2][1] = {180, 224, 247, 112, 70, 205, 212, 70}
	aY[1] = ""
	cm = 3347629
	aU[1] = {2877465, 1667491, 179, 125, 229}
	local dN
	cC[1] = dG
	co = cs[1]
	cj[1] = dJ[1]
	cs[1] = {180, 224, 247, 112, 70, 205, 212, 70}
	nx = true
	aY[1] = "tonumber"
	fo = "tonumber"
	local dN
	dG = ci
	dN = 1
	aN[424][1][1] = "Wait"
	cl[1] = 1
	nx = true
	cm = ce(aN[424][3][1],aY[1],aN[424][2][1])
	eU = cm
	local dN
	dN = "table"
	cr = {180, 224, 247, 112, 70, 205, 212, 70}
	cs[1] = ci
	ci = "table"
	dN = aW
	aW = aV
	aV = dN
	nx = true
	aN[424][2][1] = 12060276
	aY[1] = {1908913, 2794097, 91, 171, 79}
	aN[424][3][1] = {69, 206, 182, 39, 175, 17, 152, 79, 209, 247}
	cl[1] = 1
	cm = ""
	local dN
	dN = {69, 206, 182, 39, 175, 17, 152, 79, 209, 247}
	aN[424][3][1] = cs[1]
	cs[1] = {69, 206, 182, 39, 175, 17, 152, 79, 209, 247}
	dN = dJ[1]
	dJ[1] = 12060276
	aN[424][2][1] = dN
	nx = true
	cm = "StatusCode"
	eN = "StatusCode"
	local dN
	cj[1] = {2877465, 1667491, 179, 125, 229}
	dN = "Wait"
	aN[424][1][1] = aN[424][2][1]
	aN[424][2][1] = "Wait"
	nx = true
	ch[1] = nil
	local dN
	cq[1] = aN[424][1][1]
	aN[424][1][1] = ct[1]
	dN = aN[424][3][1]
	aN[424][3][1] = 1
	aN[424][4][1] = dN
	dN = {180, 224, 247, 112, 70, 205, 212, 70}
	cr = dG
	dG = true
	dC[1] = {180, 224, 247, 112, 70, 205, 212, 70}
	nx = true
	nx = true
	local dN
	aW = {69, 206, 182, 39, 175, 17, 152, 79, 209, 247}
	dN = "table"
	aN[424][2][1] = 1
	ci = "Wait"
	aN[424][4][1] = cr
	cr = "table"
	dN = ck
	ck = aN[424][1][1]
	aN[424][1][1] = dN
	dN = {2877465, 1667491, 179, 125, 229}
	cq[1] = cj[1]
	cj[1] = {2877465, 1667491, 179, 125, 229}
	nx = true
	-- region end
	-- warn: no leaf for key (408413, 86320)
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @22357
	aM = aK
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @24502
	return jD(aN[534][11],fu,fv,aN[534][14],aN[534][6],aW,fw,aN[534][4],aX,dJ,aY,fx,aN[534][18],aN[534][17],aN[534][12],cu,dC,aN[534][9],co,cC,cx,...)end
	fD = 269139
	aN[534][17][1] = ck[1]
	fD = 272194
	dE[1] = function(...)local mX=function(...)
	-- for-dispatch over nK=789..903 step 3
	aN = {}
	aH = 1649
	aN[795-136]=795+3033
	aN[(798-798)+871]=798+4914
	aM = true
	aN[829] = 2657
	aN[(620+105)-105]=807~=801
	aN[(783+215)-215]=810+9370
	aN[813] = 4382
	aN[(840+309)-309]=819+712
	aN[695] = 6827
	aN[(825-825)+639]=825+3712
	aN[(669+326)-326]=828+8124
	aN[831-226]=831+6546
	aN[703] = 3764
	aN[840-779]=840~=840
	aN[(843-843)+757]=843+2854
	aN[846+29]=846+3862
	aN[849-95]=849+7336
	aN[755] = 3139
	aN[730] = true
	aN[858-187]=858+3524
	aN[(716+38)-38]=861+1432
	aN[720] = 6063
	aN[867-814]=91031
	aN[870-862]=not false
	aN[893] = 8240
	aN[(816+43)-43]=879+4555
	aN[(761+256)-256]=882~=879
	aN[645] = 10764
	aN[600] = true
	aN[(625+139)-139]=891+5841
	aN[830] = 5033
	aW = function(...)
	ci[1] = fR
	ch = fS
	-- REGION missing init pair (cx,cC)
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @10244
	aX = aW
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @12611
	return mX(aN[534][11],fu,fv,aN[534][14],aN[534][6],aW,fw,aN[534][4],aX,dJ,aY,fx,aN[534][18],ck,aN[534][17],aN[534][12],cu,dC,aN[534][9],co,cC,cx,...)end
	fD = 267629
	fD = 273041
	do local dN;cg=ct[1];dN=fr[1];fr[1]=cA;cA=dN;end
	fE = true
	fF,fG=fD+1192460,96676+fD
	fJ = 582328
	end else
	-- sub-region (fF,fG) base fD:
	aN[534][20][1] = ce(cr[1],aN[534][8][1],aN[534][1][1])
	eS = aN[534][20][1]
	local dN
	dN = nil
	aV = nil
	ch[1] = aN[534][20][1]
	aN[534][20][1] = nil
	aN[534][21][1] = nil
	fE = true
	ch[1] = ""
	aN[534][1][1] = 5293402
	cr[1] = {3}
	aN[534][7][1] = 1
	aN[534][8][1] = {103837, 902827, 231, 163, 171}
	local dN
	dN = nil
	aN[534][21][1] = nil
	cg = nil
	dN = nil
	aN[534][20][1] = "Wait"
	aU[1] = nil
	dN = 1
	cq[1] = nil
	aN[534][23][1] = 1
	fE = true
	while aN[223]do aN[1046]=aN[85];end
	fE = true
	fE = true
	-- sub-region (fF,fG) base fD:
	-- sub-region (fF,fG) base fD:
	if not((fF-fD)>1413007)then if not((fF-fD)>=1402765)then if(fF-fD)>1293068 then if 1336235>=(fF-fD)then if(fF-fD)~=1336236 then if not((fG-fD)~=53856)then if fo==nil then aN[534][22][1]=ce(cr[1],aN[534][8][1],aN[534][1][1]);fo=aN[534][22][1];end;fD=fD+3179;fD=(fD+5006);do local dN;ct[1]=cr[1];dN=cp[1];cp[1]=cn;cn=dN;end;fE=true;fF,fG=1336235+fD,fD+67617;fJ=fF;elseif(fG-fD)==67617 then aN[534][14][1]=function(...)local ob=function(...)
	-- for-dispatch over oc=428..358 step -2
	aH = 0
	aN = {}
	aN[424+270]=424~=418
	aH = 1356
	aN[(818+498)-498]=420+7378
	aN[789] = 1022
	aM = true
	aN[414+326]=414+6167
	aN[412+442]=412+7473
	aN[410+486]=410~=416
	aN[660] = 8634
	aN[(406-406)+646]=406+9758
	aN[(404-404)+872]=404+5658
	aN[651] = true
	aN[838] = true
	aN[398+465]=398+7458
	aN[(396-396)+616]=396+278
	aN[394+359]=394+7494
	aN[392+268]=392+2585
	aN[390+233]=390~=414
	aN[857] = 7878
	aN[386+283]=386+5196
	aN[384-375]=true
	aN[382-234]=891554
	aN[(380-380)+880]=380+2092
	aN[378+365]=378+9540
	aN[613] = 10200
	aN[221] = false
	aN[818] = true
	aN[370+408]=370~=422
	aN[(368-368)+700]=368+3303
	aN[366+268]=366+4106
	aN[774] = true
	cg = function(...)
	cj = fK
	-- REGION missing init pair (cu,cx)
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @5614
	aV = cg
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @7763
	return ob(fu,fv,aW,fw,aX,fx,aN[534][18],cu,dC,co,...)end
	fD = 264305
	fr[1] = nil
	aW[1] = nil
	aW[1] = nil
	fD = 273617
	aN[534][4][1] = function(...)local oe=function(...)
	-- for-dispatch over of=907..619 step -8
	aH = 0
	aH = 0
	aN = {}
	aH = 1359
	aM = true
	aN[(663+449)-449]=867~=731
	aN[859-251]=859~=627
	aN[(851-851)+806]=851+3102
	aN[738] = true
	aN[174] = false
	aN[819+72]=819+4985
	aN[(811-811)+665]=811~=755
	aN[803-119]=803~=835
	aN[761] = 8243
	aN[787-76]=787+3792
	aN[(779-779)+877]=779+7359
	aN[(764+361)-361]=771+839
	aN[763-92]=763+916
	aN[755-50]=755+7494
	aN[135] = true
	aN[660] = 1964
	aN[731-127]=731+1448
	aN[(670+465)-465]=723+6995
	aN[715+51]=715+9786
	aN[(707-707)+865]=707+695
	aN[697] = 3183
	aN[(691-691)+873]=691+1552
	aN[675-5]=675+6367
	aN[(789+200)-200]=667+4652
	aN[(862+39)-39]=659+4981
	aN[857] = 4595
	aN[(643-643)+203]=55639
	aK = function(...)
	aV[1] = fD
	aN[199] = getfenv
	aN[211] = string
	aN[207] = string.char
	od = true
	aN[29] = "format"
	aN[100] = string[aN[29]]
	od = true
	cq[1] = 1
	aV[1] = 7529178
	aN[476][4][1] = {2116533, 2005781, 57, 49, 55}
	aW[1] = ""
	aN[476][3][1] = {3, 30, 202, 188, 208, 219, 252, 28}
	local dN
	dN = nil
	cr = nil
	cg[1] = nil
	dN = nil
	aY = ""
	aW[1] = nil
	dN = cs
	cs = 7529178
	aV[1] = dN
	od = true
	aN[958] = aN[203]+398
	aY = "tonumber"
	fo = "tonumber"
	local dN
	dN = {2116533, 2005781, 57, 49, 55}
	aN[476][4][1] = 12872556
	ct[1] = {2116533, 2005781, 57, 49, 55}
	dN = ck[1]
	ck[1] = 7529178
	cs = dN
	od = true
	cl = getfenv[fo]
	aW[1] = cl(aN[476][4][1])
	co[1] = aW[1]
	cl = aN[476][4][1]-(aN[476][4][1]//aW[1])*aW[1]
	cf[1] = 0
	cg[1] = (if aN[203]==55639 then cl~=cf[1]else aN)
	cs = (if cg[1]then not aN[135]else not aN[174])
	if aN[203]==55639 then
	dJ = 818493
	cn[1],ck[1],aN[476][2][1],cq[1],aW[1],co[1],ci[1],aN[476][1][1],aV[1],aX=aV[1],co[1],ci[1],cn[1],cl,aW[1],aX,ck[1],cq[1],aN[476][2][1]
	od = true
	cu = 1550992
	cx = 858520
	dE = 1666917
	else
	aN[1072] = nil
	end
	cl = 786417
	cq[1] = cr-(cr//cl)*cl
	co[1] = cq[1]
	cq[1] = cr-co[1]
	cs = 10713
	aN[476][3][1] = co[1]-cs
	ci[1] = 142985
	cm[1] = aN[476][3][1]*ci[1]
	cp[1] = 786417
	aW[1] = 786417
	aX = 786417
	ch[1] = cm[1]-(cm[1]//aX)*aX
	cn[1] = ch[1]+cq[1]
	cl = cn[1]
	cr = nil
	cr = (if aN[174]then aN[495]else cl)
	local dN
	ck[1] = 786417
	dN = cn[1]
	cn[1] = cq[1]
	cq[1] = dN
	od = true
	od = true
	local dN
	aN[476][1][1] = cm[1]
	cm[1] = aV[1]
	aV[1] = cq[1]
	aN[476][2][1] = aN[476][4][1]
	cq[1] = 0
	cf[1] = 786417
	dN = aW[1]
	aW[1] = co[1]
	co[1] = dN
	od = true
	cn[1] = 786417
	aN[476][2][1] = ci[1]/cn[1]
	co[1] = aN[476][2][1]
	ck[1] = co[1]
	cr = ck[1]
	aN[476][3][1] = 12347
	ci[1] = cr-aN[476][3][1]
	cn[1] = 41
	aN[476][2][1] = ci[1]/cn[1]
	co[1] = aN[476][2][1]
	aN[476][3][1] = cr-co[1]
	ci[1] = 37
	cn[1] = {}
	cn[1] = (if aN[174]then aN[511]else aN[476][3][1]/ci[1])
	return cn[1]
	while aN[174]do aN[924]=aN[203];end
	cp[1] = (if aN[203]==55639 then 9187 else 1610093)
	ck[1] = cp[1]
	cn[1] = ck[1]
	od = true
	if aN[203]==55639 then
	ci[1] = nil
	ci[1] = (if aN[135]then cr-cn[1]else aN[523])
	cp[1] = 43
	dJ = 824561
	dJ = 813725
	do local dN;cj[1]=co[1];co[1]=aW[1];aW[1]=aX;dN=aN[476][3][1];aN[476][3][1]=cn[1];cn[1]=dN;end
	od = true
	cu = 1460205
	cx = 856238
	dE = 1666917
	else
	aN[1008] = nil
	end
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @5142
	aI = aK
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @7428
	return oe(fu,fv,aN[534][14],aW,fw,aX,fx,aN[534][18],cu,dC,co,...)end
	aN[534][14][1] = nil
	fD = 267908
	fD = 264201
	aN[534][22][1],aN[534][21][1],cp[1],cA=cA,cp[1],aN[534][21][1],aN[534][22][1]
	fE = true
	fF,fG=(fD-859)+(1336235+859),(fD-219)+(25605+219)
	fJ = 582328
	elseif not(25605~=(fG-fD))then
	repeat aY[1]=fw[1];cC[1]=bf;aN[534][11][1]=aY[1][cC[1]];dJ[1]=eG;aN[534][4][1]=aN[534][11][1](aY[1],dJ[1]);fD=32214+fD;cC[1]=(if aN[85]==631730 then aN[54][bM]else aN[552]);aN[534][11][1]=cC[1];cn=(if cC[1]then not aN[30]else aN[30]);fD=(fD+15225);if cn then fD=(5902+fD);cg,ct[1],ch[1],cr[1]=aN[534][21][1],ch[1],aU[1],ct[1];fE=true;fF=fD+1336235;fG=fD+46989;fJ=fF;else fD=fD+2239;do local dN;cg=aN[534][21][1];cr[1]=ct[1];ct[1]=ch[1];ch[1]=aU[1];dN=fr[1];fr[1]=aN[534][20][1];aN[534][20][1]=dN;end;fE=true;fF=fD+1621850;fG=89012+fD;fJ=fF;end;until aN[30]
	elseif(fG-fD)==46989 then fD=(fD+3805)
	do local dN;dN=fr[1];fr[1]=aN[534][20][1];aN[534][20][1]=aN[534][23][1];aN[534][23][1]=dN;dN=cA;cA=cn;cn=cg;cg=dN;end
	fE = true
	fF,fG=fD+1528641,58926+fD
	fJ = 582328
	end end else
	-- sub-region (fF,fG) base fD:
	aN[534][20][1] = nil
	aN[534][20][1] = nil
	aU[1] = true
	local dN
	ct[1] = nil
	dN = nil
	ft[1] = nil
	cp[1] = nil
	aN[534][20][1] = nil
	cA = nil
	dN = nil
	cf = true
	aU[1] = nil
	cr[1] = nil
	fE = true
	aN[940] = 631820
	cA = nil
	ft[1] = nil
	local dN
	dN = nil
	cp[1] = nil
	ft[1] = nil
	dN = nil
	cA = nil
	aN[534][20][1] = nil
	fE = true
	cl[1] = nil
	aN[534][20][1] = nil
	aX[1] = nil
	aN[534][20][1] = nil
	cp[1] = nil
	fE = true
	-- sub-region (fF,fG) base fD:
	cn = not cu[1]
	aU[1] = cn
	aN[534][16][1] = aU[1]
	fE = true
	cr[1] = nil
	aU[1] = ""
	cn = cu[1]~=aU[1]
	aN[534][3][1] = not(if aN[85]==631730 then cn else aN[594])
	cp[1] = aN[534][3][1]
	fE = true
	aN[534][21][1] = cp[1]
	local dN
	ct[1] = nil
	dN = aN[534][21][1]
	aN[534][21][1] = nil
	cg = dN
	dN = nil
	aN[534][20][1] = nil
	cr[1] = nil
	fE = true
	if cg then
	fD = 345531
	do local dN;dN=cA;cA=aV;aV=dN;dN=cr[1];cr[1]=aU[1];aU[1]=dN;end
	fE = true
	fF = 572268
	fG = 419659
	fJ = 1629281
	else
	fD = 344036
	do local dN;cn=aN[534][21][1];aN[534][21][1]=ft[1];fr[1]=cq[1];ch[1]=aU[1];ft[1]=cA;cA=aV;cq[1]=cr[1];aU[1]=cf;cf=ct[1];ct[1]=cp[1];cp[1]=aN[534][20][1];end
	fE = true
	fF = 445439
	fG = 344982
	fJ = 1629281
	end
	-- sub-region (fF,fG) base fD:
	fE = true
	local dN
	cg = nil
	dN = nil
	aN[534][20][1] = nil
	aV = nil
	fE = true
	local dN
	cA = 1
	dN = nil
	fr[1] = nil
	cn = nil
	cg = nil
	dN = nil
	cf = nil
	aN[534][23][1] = nil
	fE = true
	aN[997] = 631883
	aU[1] = ""
	aN[534][1][1] = 5209497
	aN[534][7][1] = 1
	aN[534][8][1] = {3459761, 18987, 169, 47, 163}
	fr[1] = {204, 153, 179, 243, 174, 185, 198}
	fE = true
	aU[1] = "connect"
	eV = "connect"
	local dN
	aN[534][23][1] = nil
	dN = "connect"
	aU[1] = nil
	ch[1] = "connect"
	dN = nil
	aN[534][20][1] = nil
	cr[1] = nil
	fE = true
	aN[534][1][1] = 2351880
	aN[534][7][1] = 1
	cn = {129, 239}
	ch[1] = ""
	aN[534][8][1] = {2093973, 1078611, 121, 13, 215}
	fE = true
	ch[1] = "R1"
	eM = "R1"
	fE = true
	-- sub-region (fF,fG) base fD:
	cg = {201, 189, 8, 37}
	aN[534][21][1] = ""
	aN[534][1][1] = 11548670
	aN[534][7][1] = 1
	aN[534][8][1] = {1350493, 231167, 73, 171, 187}
	fE = true
	aU[1] = ""
	aN[534][8][1] = {2853149, 1596283, 225, 45, 181}
	aN[534][22][1] = {217}
	aN[534][1][1] = 16748233
	aN[534][7][1] = 1
	fE = true
	aU[1] = "c"
	bx = "c"
	local dN
	dN = nil
	cq[1] = {217}
	aN[534][22][1] = nil
	aN[534][23][1] = 1
	aN[534][20][1] = nil
	fE = true
	if bQ = =nil then
	aN[534][7][1] = 1
	aN[534][8][1] = {813461, 1925437, 81, 233, 23}
	aN[534][1][1] = 9146851
	cq[1] = {253, 205, 139, 21, 197, 254}
	aU[1] = ""
	end
	fE = true
	if bQ = =nil then
	aU[1] = "c"
	bQ = "c"
	end
	fE = true
	-- sub-region (fF,fG) base fD:
	aN[534][21][1] = cc(cA,aN[534][8][1],aN[534][1][1])
	eG = aN[534][21][1]
	local dN
	fr[1] = nil
	cn = 1
	dN = nil
	cp[1] = nil
	aN[534][23][1] = nil
	ft[1] = nil
	fE = true
	aN[534][7][1] = 1
	cA = {47, 212, 240, 114}
	aN[534][8][1] = {898641, 3669807, 219, 125, 33}
	aN[534][1][1] = 9561943
	aN[534][21][1] = ""
	local dN
	cq[1] = nil
	dN = {47, 212, 240, 114}
	cA = nil
	cp[1] = nil
	aN[534][23][1] = {47, 212, 240, 114}
	dN = 1
	cn = nil
	ft[1] = 1
	fE = true
	aN[534][21][1] = "warn"
	fq = "warn"
	fE = true
	aN[534][21][1] = cb(aN[534][22][1],aN[534][8][1],aN[534][1][1])
	fp = aN[534][21][1]
	fE = true
	aN[534][8][1] = {2333549, 3613703, 231, 59, 201}
	aN[534][1][1] = 11599588
	aN[534][7][1] = 1
	aN[534][22][1] = {143, 187, 92, 57, 203, 65, 22, 45}
	aN[534][21][1] = ""
	local dN
	dN = nil
	cA = nil
	aU[1] = nil
	fE = true
	aN[534][21][1] = "reported"
	fi = "reported"
	fE = true
	repeat if fg==nil then aN[534][1][1]=((fD+8070323)-(fD+257627));aN[534][8][1]={((fD+1045505)-(fD+249652)),((fD+1360258)-(fD+778227)),((fD+260902)-(fD+260811)),((fD+533120)-(fD+533047)),((fD+140350)-(fD+140273))};aN[534][21][1]='';cA={24,147};aN[534][7][1]=1;end;fD=(fD+8859);fD=(fD+621);cg,fr[1],aN[534][21][1],cf,ch[1]=fr[1],cg,ch[1],cp[1],aN[534][21][1];fE=true;fF=(fD-990)+(1763745+990);fG=fD+10799;fJ=fF;until aN[30]
	repeat if fg==nil then ch[1]=ce(cA,aN[534][8][1],aN[534][1][1]);fg=ch[1];end;fD=(fD+9376);fD=(4124+fD);do local dN;aV=aN[534][22][1];dN=cr[1];cr[1]=fr[1];fr[1]=dN;dN=aN[534][23][1];aN[534][23][1]=aN[534][20][1];aN[534][20][1]=ft[1];ft[1]=dN;end;fE=true;fF=(fD-259)+(1688974+259);fG=fD+83054;fJ=fF;until aN[30]
	while aN[223]do aN[937]=aN[85];end
	cA = {13, 124, 199, 49}
	aN[534][8][1] = {1148025, 1983219, 151, 177, 237}
	ch[1] = ""
	aN[534][1][1] = 5303261
	aN[534][7][1] = 1
	local dN
	dN = ""
	ch[1] = nil
	cg = nil
	ct[1] = nil
	aV = ""
	fE = true
	aV = "gone"
	eX = "gone"
	fE = true
	aN[534][8][1] = {3593325, 925009, 45, 79, 155}
	cq[1] = {79}
	fr[1] = ""
	aN[534][7][1] = 1
	aN[534][1][1] = 15048722
	fE = true
	fr[1] = "n"
	ff = "n"
	local dN
	cp[1] = nil
	cr[1] = "warn"
	fE = true
	cf = ci[1]
	aN[534][20][1] = cf
	local dN
	cq[1] = "n"
	cA = nil
	dN = nil
	aU[1] = nil
	cn = nil
	fE = true
	repeat cl[1]=aN[534][20][1];cu[1],cl[1]=cl[1],aX[1];fD=fD+17344;if not aX[1]then fD=(5816+fD);do local dN;aV=cA;cA=cq[1];cq[1]=cn;ct[1]=aN[534][23][1];aN[534][23][1]=aN[534][20][1];aN[534][20][1]=cp[1];end;fE=true;fF=66184+fD;fG=(fD-554)+(4889+554);fJ=fF;else fD=(5029+fD);do local dN;ct[1]=aN[534][23][1];aN[534][23][1]=aN[534][20][1];aN[534][20][1]=cp[1];aV=cn;end;fE=true;fF=fD+44093;fG=fD+18884;fJ=fF;end;until aN[30]
	local dN
	aN[534][21][1] = cf
	cf = nil
	cn = nil
	fE = true
	aN[534][6][1] = aN[54][bI]
	aN[534][17][1] = nil
	aN[534][17][1] = nil
	ck[1] = (if aN[85]==631730 then aN[534][6][1]else aN[597])[(if aN[85]~=631730 then aN else aN[534][17][1])]
	cx[1] = (if aN[85]~=631730 then aN[571]else ck[1])
	local dN
	dN = nil
	cn = {79}
	aV = nil
	dN = nil
	aN[534][22][1] = "warn"
	ch[1] = nil
	cf = nil
	fE = true
	while aN[223]do aN[949]=aN[85];end
	aN[534][20][1] = nil
	aN[534][12][1] = nil
	fE = true
	if bb = =nil then
	aN[534][1][1] = 15945342
	aU[1] = ""
	aN[534][8][1] = {211613, 3077751, 221, 39, 11}
	aN[534][23][1] = {}
	aN[534][7][1] = 1
	end
	fE = true
	while aN[223]do aN[970]=aN[85];end
	if bb = =nil then
	aU[1] = ce(aN[534][22][1],aN[534][8][1],aN[534][1][1])
	bb = aU[1]
	end
	fE = true
	aN[534][21][1] = ""
	aN[534][1][1] = 12390135
	aN[534][7][1] = 1
	aN[534][8][1] = {2026917, 198927, 187, 125, 129}
	aN[534][23][1] = {104, 52, 235, 181}
	fE = true
	aU[1] = "task"
	bR = "task"
	local dN
	cf = cq[1]
	dN = nil
	ct[1] = nil
	cA = nil
	fE = true
	repeat if bV==nil then aU[1]='';aN[534][8][1]={((fD+2284411)-(fD+427846)),((fD+1383268)-(fD+609707)),((fD+825550)-(fD+825471)),((fD+404881)-(fD+404788)),((fD+42304)-(fD+42141))};aN[534][1][1]=((fD+1240038)-(fD+497529));aN[534][7][1]=1;aN[534][23][1]={(128+17)-17,88,(105+14)-14,242};end;fD=(668+fD);fD=fD+4265;cg,ct[1],ft[1],aN[534][20][1]=ft[1],aN[534][20][1],aN[534][21][1],ct[1];fE=true;fF,fG=fD+1903999,(fD-421)+(93652+421);fJ=fF;until aN[30]
	if bV = =nil then
	aU[1] = cc(aN[534][23][1],aN[534][8][1],aN[534][1][1])
	bV = aU[1]
	end
	local dN
	aN[534][21][1] = nil
	cA = "warn"
	aV = nil
	dN = ch[1]
	ch[1] = {79}
	ft[1] = dN
	fE = true
	while aN[223]do aN[1054]=aN[85];end
	cp[1] = not aU[1]
	aN[534][20][1] = nil
	aN[534][22][1] = nil
	aU[1] = 1
	aN[534][13][1] = 1
	cg = 1
	aN[534][3][1] = 1
	cj[1] = 1696457
	fs[1] = nil
	dG[1] = (if not aN[30]then aN[577]else aN[534][9][1])(aN[534][20][1],aN[534][22][1],aU[1],aN[534][3][1],cj[1],fs[1])
	aN[534][20][1] = fx[1]
	aN[534][22][1] = nil
	aU[1] = nil
	aN[534][13][1] = nil
	aN[534][13][1] = true
	cg = true
	aN[534][3][1] = true
	local dN
	dN = nil
	aV = nil
	aN[534][22][1] = nil
	fE = true
	cj[1] = nil
	fs[1] = nil
	ch[1] = false
	dG[1] = true
	cg = true
	ci[1] = true
	fE = true
	aN[931] = 632575
	cn = bZ(aU[1],aN[534][8][1],aN[534][1][1])
	eR = cn
	fE = true
	aN[534][7][1] = 1
	aN[534][1][1] = 727061
	aN[534][8][1] = {1473285, 2932805, 55, 167, 81}
	cn = ""
	cg = {230, 194, 100, 124}
	fE = true
	cn = "acks"
	eP = "acks"
	local dN
	aN[534][21][1] = "acks"
	dN = "n"
	fr[1] = true
	aN[534][22][1] = "n"
	fE = true
	local dN
	dN = aN[534][20][1]
	aN[534][20][1] = nil
	ct[1] = aN[534][23][1]
	aN[534][23][1] = dN
	dN = "warn"
	cA = "acks"
	cn = {230, 194, 100, 124}
	cg = "warn"
	fE = true
	cq[1] = cb(aN[534][21][1],aN[534][8][1],aN[534][1][1])
	eY = cq[1]
	fE = true
	aN[534][21][1] = {133, 211, 146, 98, 15, 68, 228, 5, 128, 69, 242, 229, 145, 10, 128, 31, 87, 123, 178, 34, 251, 146, 57, 141, 119, 68, 238, 181, 85, 13, 230, 94, 89, 2, 227, 213, 0, 183, 219, 54, 100, 108, 92, 110, 36, 200, 139, 230}
	aN[534][8][1] = {2017561, 1480757, 161, 121, 109}
	cq[1] = ""
	aN[534][7][1] = 1
	aN[534][1][1] = 4029511
	fE = true
	fr[1] = "PolSec: unable to connect. Please execute again."
	eL = "PolSec: unable to connect. Please execute again."
	local dN
	aN[534][22][1] = cp[1]
	dN = {230, 194, 100, 124}
	cA = aN[534][23][1]
	aN[534][23][1] = {230, 194, 100, 124}
	fE = true
	dL[1] = (if aX[1]then not aN[30]else aN[85]==631730)
	aN[534][16][1] = dL[1]
	if dL[1] then
	fD = 932962
	do local dN;aN[534][22][1]=cn;cq[1]=ct[1];ct[1]=aN[534][21][1];aN[534][21][1]=cf;dN=ch[1];ch[1]=aV;aV=cg;cg=ft[1];ft[1]=aN[534][20][1];aN[534][20][1]=cr[1];cr[1]=dN;end
	fE = true
	fF = 2487489
	fG = 1007785
	fJ = 2459931
	else
	fD = 931112
	do local dN;dN=aV;aV=ft[1];ft[1]=dN;dN=cf;cf=ct[1];ct[1]=dN;dN=cr[1];cr[1]=ch[1];ch[1]=dN;end
	fE = true
	fF = 2487489
	fG = 1011723
	fJ = 2459931
	end
	ch[1] = aN[54][bV]
	local og=(if not aN[30]then aN[535]else ch[1])
	aN[534][20][1] = og(cu[1])
	aV = "string"
	aN[534][3][1] = (if aN[85]~=631730 then aN else(if aN[534][20][1]~=aV then aN[30]else aN[223]))
	fE = true
	cA = aN[534][3][1]
	aN[534][16][1] = cA
	local dN
	cq[1] = cf
	aN[534][22][1] = "acks"
	dN = ct[1]
	ct[1] = {133, 211, 146, 98, 15, 68, 228, 5, 128, 69, 242, 229, 145, 10, 128, 31, 87, 123, 178, 34, 251, 146, 57, 141, 119, 68, 238, 181, 85, 13, 230, 94, 89, 2, 227, 213, 0, 183, 219, 54, 100, 108, 92, 110, 36, 200, 139, 230}
	aN[534][21][1] = dN
	fE = true
	cj[1] = aN[534][16][1]
	if not aN[534][16][1] then
	fD = 932226
	aU[1],aN[534][20][1],aN[534][23][1],cg,aV,aN[534][22][1],ct[1]=ct[1],aV,aN[534][20][1],aN[534][22][1],aN[534][23][1],cg,aU[1]
	fE = false
	fF,fG,fH,fI=fD+1659399,(fD-867)+(33403+867),fD+1301193,94537+fD
	fJ = 2459931
	fK = 1687486
	else
	fD = 937675
	do local dN;dN=aN[534][23][1];aN[534][23][1]=aN[534][20][1];aN[534][20][1]=dN;dN=aU[1];aU[1]=ct[1];ct[1]=dN;end
	fE = true
	fF = 2588640
	fG = 1016335
	fJ = 2459931
	end
	cp[1] = true
	fE = true
	local dN
	aN[534][22][1] = cq[1]
	cq[1] = true
	cp[1] = "acks"
	cn = false
	cr[1] = "PolSec: unable to connect. Please execute again."
	fr[1] = aN[534][20][1]
	aN[534][20][1] = aN[534][23][1]
	dN = nil
	ct[1] = ft[1]
	ft[1] = nil
	dN = "warn"
	aV = cf
	cf = ch[1]
	ch[1] = cA
	cA = "warn"
	fE = true
	while aN[223]do aN[1043]=aN[85];end
	local dN
	dN = "warn"
	cA = cf
	cf = "warn"
	fE = true
	fE = true
	fE = true
	ch[1] = bZ(cr[1],aN[534][8][1],aN[534][1][1])
	bz = ch[1]
	fE = true
	ch[1] = ""
	aN[534][8][1] = {3487365, 3178193, 55, 185, 243}
	aN[534][1][1] = 5224543
	cg = {21, 157, 45, 121, 23, 97, 240}
	aN[534][7][1] = 1
	local dN
	cp[1] = fr[1]
	cn = nil
	fr[1] = cq[1]
	dN = {21, 157, 45, 121, 23, 97, 240}
	cg = aV
	aV = ""
	ch[1] = aN[534][20][1]
	aN[534][20][1] = {21, 157, 45, 121, 23, 97, 240}
	fE = true
	aV = "request"
	bM = "request"
	fE = true
	local dN
	dN = nil
	ct[1] = "request"
	aV = "PolSec: unable to connect. Please execute again."
	aN[534][20][1] = nil
	dN = cA
	cA = false
	aN[534][23][1] = cg
	cg = true
	aN[534][22][1] = dN
	fE = true
	fs[1] = ""
	dG[1] = fs[1]==cu[1]
	cj[1] = dG[1]
	local dN
	dN = aN[534][23][1]
	aN[534][23][1] = aN[534][22][1]
	aN[534][22][1] = dN
	fE = true
	dJ[1] = aN[54][bJ]
	aN[534][11][1] = dJ[1]
	local dN
	dN = "request"
	ct[1] = nil
	aN[534][20][1] = "request"
	fE = true
	aN[534][12][1] = aN[534][11][1]
	cA = nil
	cA = (if aN[85]~=631730 then aN[574]else not aN[534][11][1])
	if {0, 56, 164} then
	fD = 938953
	do local dN;dN=cn;cn=aN[534][22][1];aN[534][22][1]=dN;dN=ch[1];ch[1]=cr[1];cr[1]=dN;end
	fE = true
	fF = 2457882
	fG = 977717
	fJ = 2459931
	else
	fD = 934028
	ch[1],aN[534][23][1],ft[1],cr[1],aN[534][21][1],aN[534][20][1],cn,cf,aV,aN[534][22][1]=aN[534][22][1],cn,cp[1],aN[534][20][1],ft[1],aN[534][23][1],cf,ch[1],cr[1],cg
	fE = true
	fF = 2176353
	fG = 993114
	fJ = 2459931
	end
	aN[534][9][1] = aN[54][bI]
	cx[1] = aN[534][9][1]
	cA = (if aN[534][9][1]then not aN[30]else aN[30])
	fE = true
	aN[534][1][1] = 7217552
	aN[534][8][1] = {3338277, 3663887, 87, 179, 213}
	fr[1] = ""
	aV = {144, 255, 101, 249, 111, 172, 39, 88, 184, 135}
	aN[534][7][1] = 1
	fE = true
	fr[1] = "GetService"
	bf = "GetService"
	local dN
	dN = "GetService"
	fr[1] = {144, 255, 101, 249, 111, 172, 39, 88, 184, 135}
	aV = "GetService"
	dN = true
	aN[534][21][1] = {21, 157, 45, 121, 23, 97, 240}
	cf = true
	dN = "request"
	ft[1] = cp[1]
	cp[1] = "request"
	fE = true
	while aN[223]do aN[1006]=aN[85];end
	aN[534][1][1] = 14999699
	aV = ""
	aN[534][7][1] = 1
	fr[1] = {0, 56, 164}
	aN[534][8][1] = {19753, 83297, 95, 139, 81}
	local dN
	dN = {21, 157, 45, 121, 23, 97, 240}
	aN[534][21][1] = true
	cg = {21, 157, 45, 121, 23, 97, 240}
	dN = nil
	ct[1] = ft[1]
	ft[1] = nil
	fE = true
	aV = "big"
	eT = "big"
	local dN
	aU[1] = cA
	aN[534][22][1] = true
	cA = {0, 56, 164}
	dN = {21, 157, 45, 121, 23, 97, 240}
	cg = true
	cf = {21, 157, 45, 121, 23, 97, 240}
	fE = true
	if eG = =nil then
	aN[534][8][1] = {2846473, 60173, 193, 111, 185}
	aV = ""
	aN[534][7][1] = 1
	aN[534][1][1] = 1651161
	cA = {55, 143, 115, 113, 173, 11, 41, 225, 193, 99, 52}
	end
	local dN
	aN[534][21][1] = "big"
	aV = {21, 157, 45, 121, 23, 97, 240}
	fE = true
	if nil then
	continue
	end
	-- region end
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @519766
	aL = aQ
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @522162
	)(ey,ez,eA,eB,...)end end)(ck,cu,aX,cg)
	cq[1] = cn[1]
	cg[1] = nil
	cg[1] = nil
	aW[1] = (function(oh,ey,ez,eA,eB)return function(...)return(function(...)
	-- for-dispatch over oi=709..1033 step 9
	aH = 0
	aN = {}
	aH = 889
	aN[(808+289)-289]=736~=781
	aM = true
	aN[754+45]=754+1819
	aN[763-111]=763+4158
	aN[(663+246)-246]=772~=970
	aN[781-165]=781+4943
	aN[790+67]=790+2954
	aN[853] = 3840
	aN[808-128]=808+4533
	aN[(617+98)-98]=817+1923
	aN[(78+256)-256]=826~=826
	aN[835+6]=835~=736
	aN[810] = true
	aN[853-91]=853~=736
	aN[(862-862)+600]=862~=718
	aN[871-52]=871+5421
	aN[880-784]=true
	aN[(889-889)+747]=889+8032
	aN[(907-907)+831]=907+1181
	aN[853] = true
	aN[(805+393)-393]=925+9016
	aN[839] = 8098
	aN[943-194]=943+2740
	aN[741] = 2592
	aN[(961-961)+116]=310629
	aN[970-230]=970+1230
	aN[(979-979)+637]=979+2919
	aN[988-204]=988+8640
	aN[997-306]=997+9365
	aN[(817+60)-60]=1006+8832
	aK = function(...)
	aN[424][1][1] = fz
	dJ[1] = fA
	cm[1] = fB
	-- REGION missing init pair (fF,fG)
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @154357
	aS = aK
	-- PARSE ERROR: PARSE_ERROR: bad primary 'end' @156569
	)(oh,ey,ez,eA,eB,...)end end)(ck,cu,cn,aX,cg)
	cq[1] = aW[1]
	aN[353][2][1] = nil
	aN[353][2][1] = ""
	cf = nil
	cf = ""
	aN[353][2][1] = 1
	cq[1] = nil
	cq[1] = 1
	cr[1] = 1
	return cn[1](aW[1],cf,cr[1])
	aN[927] = 405419
	aN[144] = nil
	aN[236] = nil
	aN[211] = nil
	cm[1] = nil
	cB = true
	cB = true
	aX[1] = aN[144][bV]
	cu[1] = aN[144][bP]
	local qM=aX[1]
	ck[1] = qM(cu[1])
	cg[1] = nil
	cn[1] = ck[1]~=cg[1]
	ci[1] = nil
	ch = nil
	cf = not cn[1]
	local dN
	co[1] = nil
	cx[1] = 17486107117556
	aW[1] = aN[353][4][1]
	aV[1] = 1
	aN[353][2][1] = 12872556
	cr[1] = true
	aY[1] = aN[353][1][1]
	aN[353][1][1] = nil
	cp = nil
	dN = "print"
	cl = "Wait"
	aU[1] = cf
	cf = "print"
	cB = true
	cB = true
	aN[353][2][1] = aN[144][bP]
	cx[1] = #aN[353][2][1]
	cr[1] = 12
	aV[1] = cx[1]<cr[1]
	cf = aV[1]
	local dN
	dN = cf
	cf = "Wait"
	aU[1] = dN
	dN = nil
	cp = nil
	ch = nil
	cB = true
	cp = aU[1]
	local dN
	co[1] = cx[1]
	cx[1] = aN[353][4][1]
	aY[1] = nil
	cB = true
	aN[353][3][1] = 14093277
	aN[353][1][1] = ""
	aW[1] = {79, 251, 6, 169, 61, 135}
	cp = {2054913, 3842363, 93, 51, 47}
	aV[1] = 1
	cB = true
	aN[353][1][1] = "string"
	bQ = "string"
	cB = true
	if be==nil then
	cp = {477373, 2393601, 181, 91, 129}
	cf = ""
	aN[353][3][1] = 15044010
	cm[1] = 1
	aW[1] = {2, 52, 80, 55, 155, 166, 213, 79, 234, 41, 246, 188, 28, 125, 80, 105, 30, 8, 128, 2, 167, 60, 223, 217, 12, 151, 117, 195, 201, 220, 119, 142, 21}
	end
	cB = true
	-- region end
	-- warn: repeat-until 'aN[161]' not pre-true; one-shot assumed
end

local aX = aY
return aX(...)
