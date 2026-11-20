local M24 = 16777216

local function bO(dB, dC, dD)
	local out = {}
	for i = 1, #dB do
		dD = (dD * dC[1] + dC[2]) % M24
		local F = dD + (dD // 256) * dC[4] + (dD // 65536) * dC[5]
		out[i] = ((dB[i] - F) * dC[3]) % 256
	end
	return string.char(unpack(out))
end

local function bQ(dB, dC, dD)
	local out = {}
	for i = 1, #dB do
		dD = (dD * dC[1] + dC[2] * dC[1]) % M24
		local F = dD + (dD // 256) * dC[4] + (dD // 65536) * dC[5]
		out[i] = ((dB[i] * dC[3]) - F) % 256
	end
	return string.char(unpack(out))
end

local function bU(dB, dC, dD)
	local out = {}
	for i = 1, #dB do
		dD = (dD * dC[1] - dC[2]) % M24
		local F = (dD // 65536) * dC[5] + dD + (dD // 256) * dC[4]
		out[i] = ((dB[i] + F) * dC[3]) % 256
	end
	return string.char(unpack(out))
end

local function bV(dB, dC, dD)
	local out = {}
	for i = 1, #dB do
		dD = (dD * dC[1] - dC[2] * dC[1]) % M24
		local F = dD + (dD // 256) * dC[4] + (dD // 65536) * dC[5]
		out[i] = ((dB[i] * dC[3]) + F) % 256
	end
	return string.char(unpack(out))
end

return {
	bO = bO,
	bQ = bQ,
	bU = bU,
	bV = bV,
}
