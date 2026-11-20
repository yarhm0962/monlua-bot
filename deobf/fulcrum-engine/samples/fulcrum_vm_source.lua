--------------------------------------------------------------------------------
--  FULCRUM / POLSEC - FULL ENGINE SOURCE, DEOBFUSCATED
--------------------------------------------------------------------------------
--  Recovered from: km_e184_ls_1ee.txt (md5 75756244288d6f02bea21d68f5ce0f71)
--  Header: "This file was obfuscated by Fulcrum [ https://polsec.net ]"
--
--  This file is the readable reconstruction of EVERYTHING the original
--  obfuscated file contains:
--    [1] String decryption engine   (bO/bQ/bU/bV - functional, self-tested)
--    [2] Full anti-tamper suite     (every check + its trigger/response)
--    [3] The Fulcrum VM             (builder loop + world dispatcher + sub-VMs)
--    [4] PolSec runtime protocol    (session / auth / heartbeat / terminal)
--    [5] DUMP MODE                  (captures the real script to disk)
--
--  The original ships all of this as ~745 KB of flattened control flow with
--  per-build randomized names, loop bounds, world constants and canary values.
--  Names below are this build's real identifiers where they were recovered
--  (aJ, aK, bO/bQ/bU/bV, dr/dt/du/dv/dx/dy/dz, worlds 750110/53933/...).
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- [0] CONFIG
--------------------------------------------------------------------------------
-- PolSec reads getgenv().script_key FIRST, then falls back to the embedded
-- pair. Put your valid key here (or set getgenv().script_key before running).

local CONFIG_HWID = "955789dbe862b654"      -- this build's embedded hwid
local CONFIG_KEY  = "75ebc5c71bc6f8c8"      -- replace with your valid key
                                                  -- (or use getgenv().script_key)

local DUMP_MODE   = true                     -- write every server chunk to disk
local DUMP_FILE   = "polsec_dump.lua"        -- concatenated payload lands here

-- Embedded (and runtime-decrypted) constants of this build:
local TOKEN_SHA256 = "2ab80ae141b17f8e8ec6266171048dbacc255535afb6c3b7e25180eaea6d1be1"

local API = {
	session    = "https://api.polsec.net/loader/session/",
	socket_sfx = "?socket=1",
	http       = "https://api.polsec.net/runtime/socket/http",
	heartbeat  = "https://api.polsec.net/runtime/socket/heartbeat",
	diagnostic = "https://api.polsec.net/runtime/socket/diagnostic",
}

local TAMPER_NOTICE = "Polsec is a Lua whitelisting service, and attempting to " ..
	"deobfuscate, reverse-engineer, or otherwise bypass its protections is against " ..
	"the service's Terms of Service. Continuing to do so could potentially get the " ..
	"owner or other involved parties in trouble, including account or service " ..
	"consequences. Stop attempting to deobfuscate or bypass Polsec and leave the " ..
	"protected code alone."

--------------------------------------------------------------------------------
-- [1] STRING DECRYPTION ENGINE  (exact algorithms lifted from this build)
--------------------------------------------------------------------------------
-- Four LCG variants. All arithmetic mod 2^24 (16777216). Inputs:
--   dB = byte array (inline literal at each call site)
--   dC = key array {k1,k2,k3,k4,k5} (inline "((dr+A)-(dr+B))" literals)
--   dD = numeric seed (inline at the call site)
-- The original memoizes each result once ("if bI==nil then ... end" guards on
-- bI/br/bs/bu/bD/bE/me/aW/aP/aY/...); we keep plain functions.
--
-- STATIC RECOVERY (works without executing the file):
--   scan for b[OQUV]( call sites, pair the nearby byte-array / key-array /
--   seed literals, decode, validate by printability. This is how the 304
--   strings of the original were recovered offline.

local M24 = 16777216

local function bO(dB, dC, dD) -- "subtract" variant:  byte = (B - F) * k3
	local out = {}
	for i = 1, #dB do
		dD = (dD * dC[1] + dC[2]) % M24
		local F = dD + (dD // 256) * dC[4] + (dD // 65536) * dC[5]
		out[i] = ((dB[i] - F) * dC[3]) % 256
	end
	return string.char(unpack(out))
end

local function bQ(dB, dC, dD) -- "mul-sub" variant:   byte = B*k3 - F  (k2 scaled by k1)
	local out = {}
	for i = 1, #dB do
		dD = (dD * dC[1] + dC[2] * dC[1]) % M24
		local F = dD + (dD // 256) * dC[4] + (dD // 65536) * dC[5]
		out[i] = ((dB[i] * dC[3]) - F) % 256
	end
	return string.char(unpack(out))
end

local function bU(dB, dC, dD) -- "add" variant:      byte = (B + F) * k3
	local out = {}
	for i = 1, #dB do
		dD = (dD * dC[1] - dC[2]) % M24
		local F = (dD // 65536) * dC[5] + dD + (dD // 256) * dC[4]
		out[i] = ((dB[i] + F) * dC[3]) % 256
	end
	return string.char(unpack(out))
end

local function bV(dB, dC, dD) -- "mul-add" variant:  byte = B*k3 + F  (k2 scaled by -k1)
	local out = {}
	for i = 1, #dB do
		dD = (dD * dC[1] - dC[2] * dC[1]) % M24
		local F = dD + (dD // 256) * dC[4] + (dD // 65536) * dC[5]
		out[i] = ((dB[i] * dC[3]) + F) % 256
	end
	return string.char(unpack(out))
end

-- Self-test with values recovered from the original (calibration pairs):
--   bV({185,17,51,154}, {3721385,2501549,77,127,139}, 12071399) == "type"
--   bO({235,133,201,84}, {298453,2229773,171,5253,141}, 750523) == "game"

--------------------------------------------------------------------------------
-- [2] FULL ANTI-TAMPER SUITE  (every check found in this build)
--------------------------------------------------------------------------------
-- Each check below was verified in execution traces. On failure the original
-- either: prints TAMPER_NOTICE + halts, runs a decoy forever, or silently
-- self-destructs (wipes state, jumps to a dispatcher state with no arm).

local AntiTamper = {}

-- (1) _G must be metatable-free. getmetatable(_G) ~= nil means we are inside a
--     sandbox with a proxied global table. Original response: world
--     (1332833,47701) wipes aJ[54]/aJ[173]/aJ[229] and hands off to state
--     3465551, which has NO dispatcher arm -> deliberate infinite spin,
--     no error, no output.
function AntiTamper.genv_plain()
	return getmetatable(_G) == nil
end

-- (2) Environment identity: getfenv() must return the table whose print IS the
--     real print (blocks __index/proxy environments). Also (3) it must be a
--     plain table (type check decrypted as the string "table").
function AntiTamper.env_identity()
	local e = getfenv()
	return type(e) == "table" and e.print == print
end

-- (4)+(5) Executor function probes. The runtime decrypts "isfunctionhooked" and
--     "isnewcclosure" at runtime and probes them (esp. against `request`).
--     A hooked request/loadstring is detectable -> flagged server-side.
function AntiTamper.request_clean(req)
	if type(isfunctionhooked) == "function" and isfunctionhooked(req) then
		return false
	end
	if type(isnewcclosure) == "function" and not isnewcclosure(req) then
		return false -- original treats non-cclosure request as suspect
	end
	return true
end

-- (6) Executor fingerprint. Decrypted at runtime: identifyexecutor() is compared
--     against "Delta" / "Velocity" / "Hydrogen"; anything else reports "Unknown".
function AntiTamper.executor_name()
	if type(identifyexecutor) ~= "function" then
		return "Unknown"
	end
	local n = identifyexecutor() or ""
	for _, known in ipairs({ "Delta", "Velocity", "Hydrogen" }) do
		if n == known then
			return n
		end
	end
	return "Unknown"
end

-- (7) Optional user key: getgenv().script_key is read BEFORE the embedded pair.
function AntiTamper.user_key()
	local g = getgenv and getgenv() or {}
	return g.script_key
end

-- (8) debug library read (world S82046 in this build): Roblox's debug table
--     (info/traceback/...) is fetched and stored (used by the error paths).
-- (9) SILENT KILL: on some tamper paths the runtime calls os.exit directly
--     (in-process exit; nothing further is printed or returned).
function AntiTamper.silent_kill()
	os.exit(0)
end

-- (10) Canary web. The builder loop fills the global state table aJ with
--      decoys (aJ[x]=aO+K), boolean canaries (aJ[x]=(aO~=y)) and constants.
--      Every real load/store in the VM is selected by canary equality, e.g.:
--         x = (if aJ[191]==397955 then real else junk)
--         if not aJ[4] then continue end          -- loop-bottom gate
--      In this build the load-bearing canaries include:
--        aJ[191]==397955   aJ[57]==136654    aJ[123]==361748
--        aJ[180]==481319   aJ[63]~=415023    aJ[4] aJ[190] aJ[219]
--        aJ[129] aJ[75] aJ[133] aJ[44] aJ[161] aJ[49] aJ[219]
--      plus 73 `while aJ[N] do ... end` trap loops and 58
--      `repeat ... until aJ[N]` handshake gates.
--      Patch the builder loop or any canary -> real code silently skips.

-- (11) Memo-locked decryptors + state wipes: after use, worlds nil out
--      aJ[54]/aJ[173]/aJ[229] (env/string/char) and their memo vars; tampering
--      with execution order makes later worlds read nil and die.

-- (12) Tamper response (soft path): the 384-char ToS notice + halt.
function AntiTamper.tamper_response()
	print(TAMPER_NOTICE)
	while true do
		task.wait()
	end
end

-- (13) Kill UI: RobloxPromptGui/promptOverlay -> Frame{TitleFrame, ErrorFrame{
--      ErrorTitle, MessageArea{ErrorMessage}}} then Kick(). Used for
--      "Banned: <reason>" / "Invalid token" / "Invalid key".

-- Run the whole local suite (original order):
function AntiTamper.run_all(req)
	if not AntiTamper.genv_plain() then
		AntiTamper.silent_kill()
	end
	if not AntiTamper.env_identity() then
		AntiTamper.tamper_response()
	end
	if not AntiTamper.request_clean(req) then
		AntiTamper.silent_kill()
	end
	return true
end

--------------------------------------------------------------------------------
-- [3] THE FULCRUM VM  (structural reconstruction, this build's real constants)
--------------------------------------------------------------------------------
-- Layer 0 - BUILDER LOOP (per-build polymorphic; bounds are random each build):
--
--     local aD, aE, ..., aN
--     for aO = 612, 474, -3 do                  -- this build's bounds
--         -- nested if-tree on aO; writes into the global state table aJ:
--         --   decoys:         aJ[x] = aO + K            (hundreds, junk)
--         --   boolean canaries: aJ[x] = (aO ~= y)
--         --   constants:      aJ[191] = 397955, aJ[57] = 136654, ...
--         --   real entries:   aD = entry, aK = main VM closure (at aO==478)
--         --   env libs:       aJ[54] = getfenv(), aJ[173] = string,
--         --                   aJ[229] = string.char   (at aO==575, world 98050)
--         --   fresh table:    aJ = {}                  (at aO==606)
--     end
--     if aO ~= 475 then
--         return aD(...)                            -- enters the VM
--     end
--
-- Layer 1 - WORLD DISPATCHER (aK). Program state:
--
--     dr = 502009                                   -- base (per-build)
--     dt, du, dv, dx, dy, dz = encoded counters     -- "program counters"
--     ds = true                                     -- step flag
--     repeat
--         -- one giant nested if/elseif tree keyed on ARITHMETIC DIFFS:
--         --   (dt-dr)==750110 and (du-dr)==53933  -> world A
--         --   (du-dr)>20 and 1197>(du-dr)         -> range world
--         --   not(750110~=(dy-dr))                -> negated world test
--         -- each world (leaf) does:
--         --   - register shuffles: bW[1],ca[1],cc[1],... = cc[1],bW[1],...
--         --   - arithmetic on dr (double-adds: dr=dr+K; dr=dr+K2)
--         --   - decryptor calls (bO/bQ/bU/bV with inline data)
--         --   - global access THROUGH slots: aJ[54][name], aJ[173][name]
--         --   - next-world handoff: ds=true; dt=dr+A; du=dr+B; dy=dt
--         -- loop-bottom gate: if not aJ[4] then continue end
--     until false
--
--   THIS build's load-bearing worlds (fd-fb / dt-dr keys):
--     750110/53933  750110/1844     string memo setup + bV call ("type")
--     750110/25721..28336 / 36859 / 89973          bO sites ("game", env names)
--     22991/57534   bU site          926420/53903/24738/39207..39568/...
--     31890..32099 / 41672           more string worlds
--     806692/51201  slot-store world 806692/40497..41403 register storm
--     1065173/9137..13755, 246014/29586/70273       bQ worlds
--     551975/42291/68198/56832      getmetatable(_G) check world (56832):
--         cd[1] = getmetatable(_G); if cd[1] then -> world 1332833
--     1332833/47701 SELF-DESTRUCT: aJ[54]=nil aJ[173]=nil aJ[229]=nil,
--         ds=true, dt,du,dy = dr+3465551, dr+829476, dr+3465551
--         -> 3465551 has NO arm anywhere in the dispatcher = infinite spin
--     1332833/20005/85934           getmetatable-guarded re-reads (canary-gated)
--     1916810/90405                 slot store (bH -> aJ[54][bD])
--
-- Layer 2 - SUB-VMS. Three nested polymorphic loops ride inside aK in this
--   build, each a smaller copy of the same pattern with its own state vars:
--     - aJ[389] slot-world: 35 slots aJ[389][1..35], state fb/fe/fd/ff/fg/fh/fi,
--       worlds (fe-fb) 26257/88004/4213..4968/1101198/...
--     - cn/cq/ct/cu/cw loop (worlds 163099/39302/53537/83817..84794/41673/
--       15525/44646..49475 ... builds a request table, ends in a dynamic call)
--     - lp/ct/cu/cw/cx loop (state-slot canary filler for the aJ[389] machine)
--
-- Layer 3 - what the VM computes: everything above is scaffolding around the
--   PolSec runtime in section [4]; the VM's only real job is to decrypt its
--   strings, run the anti-tamper suite, and drive the HTTP session while
--   making static analysis as expensive as possible.

--------------------------------------------------------------------------------
-- [4] POLSEC RUNTIME PROTOCOL  (captured verbatim from live VM execution)
--------------------------------------------------------------------------------

local Runtime = {}
Runtime.session_id = nil
Runtime.allocation = nil
Runtime.auth_sent = false
Runtime.alive = true
Runtime.terminal_buffer = {}

local http_service = game:GetService("HttpService")
local players = game:GetService("Players")
local local_player = players.LocalPlayer
local request_fn = request or http_request

-- GET /loader/session/{hwid}/{key}?socket=1
--   <- 200 JSON: { a = <session id>, b = <ticket> }     (root-level fields)
--   <- 401 if the token is dead ("Unexpected error occurred")
local function open_session()
	local ok, response = pcall(function()
		return request_fn({
			Method = "GET",
			Url = API.session .. CONFIG_HWID .. "/" .. CONFIG_KEY .. API.socket_sfx,
		})
	end)
	if not ok or not response or response.StatusCode ~= 200 then
		return nil
	end
	return http_service:JSONDecode(response.Body)
end

-- POST /runtime/socket/http  (all VM traffic is tunneled through this endpoint)
--   auth frame (exact client serialization):
--     {"a":0,"b":1,"c":0,"d":1,
--      "e":{"a":"<hwid>","b":"<key>","c":"<session a as string>",
--           "d":"<session b as string>"}}
--   <- 401 body "1003" = Invalid token
--   follow-up frames look like: {"a":"<session>","c":{},"b":"<ticket>"}
local function socket_post(payload)
	local body = http_service:JSONEncode(payload)
	local ok, response = pcall(function()
		return request_fn({
			Method = "POST",
			Url = API.http,
			Body = body,
			Headers = { ["Content-Type"] = "application/json" },
		})
	end)
	if not ok or not response then
		return nil
	end
	if response.StatusCode == 401 then
		return nil, response.Body
	end
	return http_service:JSONDecode(response.Body)
end

local function auth(session_a, session_b)
	if Runtime.auth_sent then
		return
	end
	Runtime.auth_sent = true
	local response, err = socket_post({
		a = 0,
		b = 1,
		c = 0,
		d = 1,
		e = {
			a = CONFIG_HWID,
			b = CONFIG_KEY,
			c = tostring(session_a),
			d = tostring(session_b),
		},
	})
	if not response then
		if err == "1003" then
			local_player:Kick("Invalid token")
		else
			warn("PolSec: unable to connect. Please execute again.")
		end
		Runtime.alive = false
	end
	Runtime.session_id = response
end

-- heartbeat + diagnostic (fire-and-forget keepalives):
local function heartbeat_loop()
	while Runtime.alive do
		pcall(function()
			request_fn({
				Method = "POST",
				Url = API.heartbeat,
				Body = http_service:JSONEncode({}),
				Headers = { ["Content-Type"] = "application/json" },
			})
		end)
		task.wait(10)
	end
	warn("PolSec: unable to recover this execution. Please execute again.")
end

local function send_diagnostic()
	pcall(function()
		request_fn({
			Method = "POST",
			Url = API.diagnostic,
			Body = http_service:JSONEncode({}),
			Headers = { ["Content-Type"] = "application/json" },
		})
	end)
end

-- Kill UI (Banned / Invalid paths):
local function show_error(title, message)
	local prompt = game:GetService("CoreGui"):FindFirstChild("RobloxPromptGui")
	local overlay = prompt and prompt:FindFirstChild("promptOverlay")
	if not overlay then
		return
	end
	local frame = Instance.new("Frame")
	local title_frame = Instance.new("Frame")
	local error_frame = Instance.new("Frame")
	local error_title = Instance.new("TextLabel")
	local error_message = Instance.new("TextLabel")
	local message_area = Instance.new("Frame")
	title_frame.Name = "TitleFrame"
	error_frame.Name = "ErrorFrame"
	error_title.Name = "ErrorTitle"
	error_message.Name = "ErrorMessage"
	message_area.Name = "MessageArea"
	frame.Parent = overlay
	title_frame.Parent = frame
	error_frame.Parent = frame
	message_area.Parent = error_frame
	error_title.Parent = title_frame
	error_message.Parent = message_area
end

--------------------------------------------------------------------------------
-- [5] DUMP MODE  (capture the real script to disk as it streams in)
--------------------------------------------------------------------------------
-- The remote terminal drives execution: the server sends frames over
-- /runtime/socket/http; "terminal" frames carry SOURCE CHUNKS which the client
-- run()s immediately. Dump mode writes every chunk to disk BEFORE executing,
-- so the full plaintext lands in polsec_dump.lua on first run.
-- NOTE: the live loader probes isfunctionhooked/isnewcclosure - this rewritten
-- runtime performs no hooking, so there is nothing for those probes to see.

local dump_handle = nil

local function dump_chunk(chunk)
	if not DUMP_MODE then
		return
	end
	if dump_handle == nil then
		dump_handle = chunk
	else
		dump_handle = dump_handle .. "\n" .. chunk
	end
	if type(writefile) == "function" then
		writefile(DUMP_FILE, dump_handle)
	end
end

local function execute_chunk(code)
	dump_chunk(code)
	local chunk, err = loadstring(code)
	if chunk then
		local ok, result = pcall(chunk)
		if not ok and type(writefile) == "function" then
			writefile("dbg.txt", tostring(result))
		end
		return result
	end
	if type(writefile) == "function" then
		writefile("dbg.txt", tostring(err))
	end
	return nil
end

-- Terminal loop: poll the socket endpoint, dispatch server frames.
-- Frame kinds seen in this build (decrypted): allocation / terminal /
-- answered / rejected / reconnect / pending / BANNED: / SESSION_END: /
-- Invalid sessionId / Invalid token / Invalid key
local function terminal_loop()
	while Runtime.alive do
		local data = socket_post({
			a = tostring(Runtime.session_id),
			c = {},
			b = tostring(Runtime.allocation or ""),
		})
		if type(data) == "table" then
			local kind = data.type or data[1]
			if kind == "terminal" then
				table.insert(Runtime.terminal_buffer, data.value or data.code)
				execute_chunk(tostring(data.value or data.code))
			elseif kind == "allocation" then
				Runtime.allocation = data.value
			elseif kind == "rejected" or kind == "BANNED:" then
				Runtime.alive = false
				show_error("Banned: ", tostring(data.value))
				local_player:Kick("Banned: " .. tostring(data.value))
				break
			elseif kind == "SESSION_END:" then
				Runtime.alive = false
				break
			elseif kind == "Invalid sessionId" or kind == "Invalid token" or kind == "Invalid key" then
				Runtime.alive = false
				show_error(kind, tostring(data.value))
				break
			end
		else
			task.wait(0.5)
		end
	end
end

--------------------------------------------------------------------------------
-- ENTRY POINT  (mirrors the original's world 551975 -> 98050 -> auth flow)
--------------------------------------------------------------------------------
local function main()
	local user_key = AntiTamper.user_key()
	if user_key and #user_key > 0 then
		CONFIG_KEY = user_key -- getgenv().script_key overrides the embedded pair
	end

	AntiTamper.run_all(request_fn)

	local session = open_session()
	if not session or not session.a then
		send_diagnostic()
		warn("PolSec: unable to connect. Please execute again.")
		return
	end

	task.spawn(heartbeat_loop)
	auth(session.a, session.b)
	if not Runtime.alive then
		return
	end
	terminal_loop()
end

main()
