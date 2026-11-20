local Fulcrum = {}

Fulcrum.BASE = 502009
Fulcrum.ENTRY_ARG = 612
Fulcrum.ENTRY_STEP = -3
Fulcrum.ENTRY_EXIT = 475
Fulcrum.ENV_SLOT = 54
Fulcrum.STRING_SLOT = 173
Fulcrum.CHAR_SLOT = 229
Fulcrum.SCRATCH = 547
Fulcrum.SUBVM_SLOT = 389
Fulcrum.SUBVM_SLOTS = 35

Fulcrum.CANARIES = {
	[191] = 397955,
	[57] = 136654,
	[123] = 361748,
	[180] = 481319,
}

Fulcrum.BOOL_CANARIES = { 4, 44, 49, 75, 129, 133, 161, 190, 219 }

Fulcrum.WORLDS = {
	SETUP_STRING = 750110,
	BV_TYPE = 53933,
	MEMO_GUARD = 1844,
	BO_GAME = 25721,
	BO_RANGE = 28336,
	BU_MEMO = 22991,
	BU_CALL = 57534,
	BQ_SETUP = 926420,
	BQ_CALL = 53903,
	REGISTER_STORM = 806692,
	SLOT_STORE = 51201,
	BQ_WORLD = 1065173,
	BQ_ALT = 246014,
	GETMT_CHECK = 551975,
	GETMT_TEST = 56832,
	WIPE = 1332833,
	WIPE_PAIR = 47701,
	SELF_DESTRUCT = 3465551,
	SLOT_WRITE = 1916810,
	SLOT_WRITE_PAIR = 90405,
}

Fulcrum.TRAP_LOOPS = 73
Fulcrum.HANDSHAKE_GATES = 58

function Fulcrum.new_state()
	local aJ = {}
	aJ[Fulcrum.SCRATCH] = {}
	for i = 1, 4 do
		aJ[Fulcrum.SCRATCH][i] = {}
	end
	return aJ
end

function Fulcrum.build(aJ, canary_ok)
	local aD = nil
	local aK = nil
	for aO = Fulcrum.ENTRY_ARG, 474, Fulcrum.ENTRY_STEP do
		if aO == 606 then
			aJ = Fulcrum.new_state()
		elseif aO == 575 then
			aJ[Fulcrum.ENV_SLOT] = getfenv()
			aJ[Fulcrum.STRING_SLOT] = string
			aJ[Fulcrum.CHAR_SLOT] = string.char
		elseif aO == 478 then
			aK = function(...) end
		elseif aO == 475 then
			aD = aK
		end
		if not canary_ok(aO) then
			return nil
		end
	end
	return aD
end

function Fulcrum.wipe(aJ)
	aJ[Fulcrum.ENV_SLOT] = nil
	aJ[Fulcrum.STRING_SLOT] = nil
	aJ[Fulcrum.CHAR_SLOT] = nil
	aJ[Fulcrum.SCRATCH][1] = nil
end

function Fulcrum.self_destruct(aJ, state)
	if state.dt == Fulcrum.WORLDS.WIPE and state.du == Fulcrum.WORLDS.WIPE_PAIR then
		Fulcrum.wipe(aJ)
		state.dt = Fulcrum.WORLDS.SELF_DESTRUCT
		state.du = 829476
		state.dy = Fulcrum.WORLDS.SELF_DESTRUCT
		return true
	end
	return false
end

function Fulcrum.step(state, worlds)
	local dt = state.dt - state.dr
	local du = state.du - state.dr
	local dv = state.dv - state.dr
	local dx = state.dx - state.dr
	local dy = state.dy - state.dr
	local dz = state.dz - state.dr
	local fn = worlds[dt] or worlds[du] or worlds[dy]
	if fn then
		fn(state, dt, du, dv, dx, dy, dz)
		return true
	end
	if Fulcrum.self_destruct(Fulcrum.aJ or {}, state) then
		return true
	end
	return false
end

return Fulcrum
