local function show(message)
    print("[Path2D capture] " .. message)
    if type(setclipboard) == "function" then
        pcall(setclipboard, message)
    end
    pcall(function()
        local root = type(gethui) == "function" and gethui() or game:GetService("CoreGui")
        local gui = Instance.new("ScreenGui")
        gui.Name = "Path2DCaptureResult"
        gui.ResetOnSpawn = false
        gui.Parent = root
        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(0, 420, 0, 100)
        label.Position = UDim2.new(0.5, -210, 0, 30)
        label.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
        label.TextColor3 = Color3.fromRGB(255, 255, 255)
        label.TextSize = 17
        label.TextWrapped = true
        label.Text = "Path2D capture\n" .. message .. "\nCopied if clipboard is available"
        label.Parent = gui
    end)
end

local ok, result = pcall(function()
    local gui = Instance.new("ScreenGui")
    local frame = Instance.new("Frame")
    frame.Position = UDim2.new(0, 0, 0, 0)
    frame.Size = UDim2.new(0, 275, 0, 145)
    frame.Parent = gui
    local path = Instance.new("Path2D")
    path.Parent = frame
    path:SetControlPoints({
        Path2DControlPoint.new(UDim2.new(0, -1, 0.5, -6), UDim2.new(-0.125, -8, 0, 2), UDim2.new(0.0625, -4, 0, 7)),
        Path2DControlPoint.new(UDim2.new(0.3125, -8, 0.5, 8), UDim2.new(0.0625, 1, -0.125, -5), UDim2.new(-0.125, -4, 0, -5)),
        Path2DControlPoint.new(UDim2.new(0.5, 1, 0.5, 8), UDim2.new(0, 0, 0, 0), UDim2.new(0, -4, 0, -1))
    })
    local length = path:GetLength()
    local size = frame.AbsoluteSize
    local text = string.format("length=%.17g; floor=%d; frame=%s", length, math.floor(length), tostring(size))
    gui:Destroy()
    return text
end)

show(ok and result or ("ERROR: " .. tostring(result)))
