local function show(message)
    print("[Path2D capture]\n" .. message)
    local copied = false
    if type(setclipboard) == "function" then
        copied = pcall(setclipboard, message)
    end
    if type(writefile) == "function" then
        pcall(writefile, "path_curve_capture.txt", message)
    end
    pcall(function()
        local root = type(gethui) == "function" and gethui() or game:GetService("CoreGui")
        local gui = Instance.new("ScreenGui")
        gui.Name = "Path2DCurveCapture"
        gui.ResetOnSpawn = false
        gui.Parent = root
        local label = Instance.new("TextLabel")
        label.Size = UDim2.new(0, 600, 0, 360)
        label.Position = UDim2.new(0.5, -300, 0, 20)
        label.BackgroundColor3 = Color3.fromRGB(25, 25, 25)
        label.TextColor3 = Color3.fromRGB(255, 255, 255)
        label.TextSize = 13
        label.TextWrapped = true
        label.TextXAlignment = Enum.TextXAlignment.Left
        label.TextYAlignment = Enum.TextYAlignment.Top
        label.Text = (copied and "Copied. Paste the result in chat.\n" or "Copy from console or send a screenshot.\n") .. message
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
    local points = {0.2857142984867096, 0.8571428656578064, 0.5333333611488342, 0.9090909361839294, 0.6666666865348816, 0.27272728085517883, 0.3636363744735718, 0.5}
    local lines = {string.format("length=%.17g", path:GetLength())}
    for _, t in ipairs(points) do
        local p = path:GetPositionOnCurve(t)
        local a = path:GetPositionOnCurveArcLength(t)
        local d = path:GetTangentOnCurve(t)
        local e = path:GetTangentOnCurveArcLength(t)
        lines[#lines + 1] = string.format("t=%.17g;p=%.17g,%d,%.17g,%d;a=%.17g,%d,%.17g,%d;d=%.17g,%.17g;e=%.17g,%.17g", t, p.X.Scale, p.X.Offset, p.Y.Scale, p.Y.Offset, a.X.Scale, a.X.Offset, a.Y.Scale, a.Y.Offset, d.X, d.Y, e.X, e.Y)
    end
    gui:Destroy()
    return table.concat(lines, "\n")
end)

show(ok and result or ("ERROR: " .. tostring(result)))
