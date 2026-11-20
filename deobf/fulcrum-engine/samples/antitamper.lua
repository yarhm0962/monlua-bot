local TAMPER_NOTICE = "Polsec is a Lua whitelisting service, and attempting to deobfuscate, reverse-engineer, or otherwise bypass its protections is against the service's Terms of Service. Continuing to do so could potentially get the owner or other involved parties in trouble, including account or service consequences. Stop attempting to deobfuscate or bypass Polsec and leave the protected code alone."

local AntiTamper = {}

function AntiTamper.genv_plain()
	return getmetatable(_G) == nil
end

function AntiTamper.env_identity()
	local e = getfenv()
	return type(e) == "table" and e.print == print
end

function AntiTamper.request_clean(req)
	if type(isfunctionhooked) == "function" and isfunctionhooked(req) then
		return false
	end
	if type(isnewcclosure) == "function" and not isnewcclosure(req) then
		return false
	end
	return true
end

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

function AntiTamper.user_key()
	local g = getgenv and getgenv() or {}
	return g.script_key
end

function AntiTamper.silent_kill()
	os.exit(0)
end

function AntiTamper.tamper_response()
	print(TAMPER_NOTICE)
	while true do
		task.wait()
	end
end

function AntiTamper.show_error(title, message)
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

return AntiTamper
