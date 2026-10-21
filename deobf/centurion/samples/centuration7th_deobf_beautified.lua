local Players = game:GetService("Players")
local SoundService = game:GetService("SoundService")
local TweenService = game:GetService("TweenService")
local Camera = Instance.new("Camera")
Camera:Destroy()
Camera:Destroy()
local Path2D = Instance.new("Path2D")
Path2D:SetControlPoints({ 1, 2 })
Path2D:Destroy()
Path2D:Destroy()
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Lighting = game:GetService("Lighting")
local StarterGui = game:GetService("StarterGui")
local hui = gethui()
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "RandomThingsHub"
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
ScreenGui.ResetOnSpawn = false
ScreenGui.IgnoreGuiInset = true
ScreenGui.Parent = hui
local Frame = Instance.new("Frame")
Frame.Active = true
Frame.Name = "Main"
Frame.Position = UDim2.new(0.5, -260, 0.5, -170)
Frame.Parent = ScreenGui
Frame.BackgroundColor3 = Color3.fromRGB(18, 18, 22)
Frame.BorderSizePixel = 0
Frame.Size = UDim2.fromOffset(520, 340)
local UICorner = Instance.new("UICorner")
UICorner.Parent = Frame
UICorner.CornerRadius = UDim.new(0, 10)
local UIStroke = Instance.new("UIStroke")
UIStroke.ApplyStrokeMode = Enum.ApplyStrokeMode.Border
UIStroke.Transparency = 0.4
UIStroke.Color = Color3.fromRGB(90, 65, 165)
UIStroke.Parent = Frame
UIStroke.Thickness = 1
local Frame2 = Instance.new("Frame")
Frame2.Name = "TitleBar"
Frame2.Parent = Frame
Frame2.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame2.BorderSizePixel = 0
Frame2.Size = UDim2.new(1, 0, 0, 36)
local UICorner2 = Instance.new("UICorner")
UICorner2.Parent = Frame2
UICorner2.CornerRadius = UDim.new(0, 10)
local Frame3 = Instance.new("Frame")
Frame3.Position = UDim2.new(0, 0, 1, -12)
Frame3.Parent = Frame2
Frame3.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame3.BorderSizePixel = 0
Frame3.Size = UDim2.new(1, 0, 0, 12)
local TextLabel = Instance.new("TextLabel")
TextLabel.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel.Parent = Frame2
TextLabel.Text = "RANDOM THINGS HUB"
TextLabel.Font = Enum.Font.GothamBold
TextLabel.BackgroundTransparency = 1
TextLabel.Position = UDim2.fromOffset(14, 0)
TextLabel.TextXAlignment = Enum.TextXAlignment.Left
TextLabel.TextSize = 14
TextLabel.Size = UDim2.new(1, -80, 1, 0)
local Frame4 = Instance.new("Frame")
Frame4.Position = UDim2.new(1, -56, 0.5, -4)
Frame4.Parent = Frame2
Frame4.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame4.BorderSizePixel = 0
Frame4.Size = UDim2.fromOffset(8, 8)
local UICorner3 = Instance.new("UICorner")
UICorner3.Parent = Frame4
UICorner3.CornerRadius = UDim.new(0, 4)
local TextButton = Instance.new("TextButton")
TextButton.TextColor3 = Color3.fromRGB(150, 150, 165)
TextButton.Parent = Frame2
TextButton.Text = "×"
TextButton.AutoButtonColor = false
TextButton.Font = Enum.Font.GothamBold
TextButton.Position = UDim2.new(1, -34, 0.5, -12)
TextButton.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
TextButton.TextSize = 16
TextButton.Size = UDim2.fromOffset(24, 24)
local UICorner4 = Instance.new("UICorner")
UICorner4.Parent = TextButton
UICorner4.CornerRadius = UDim.new(0, 6)
TextButton.MouseEnter:Connect(function(arg)
	TextButton.TextColor3 = Color3.fromRGB(230, 80, 100)
end)
TextButton.MouseLeave:Connect(function(arg2)
	TextButton.TextColor3 = Color3.fromRGB(150, 150, 165)
end)
TextButton.MouseButton1Click:Connect(function()
	ScreenGui:Destroy()
end)
local Frame5 = Instance.new("Frame")
Frame5.Name = "TabBar"
Frame5.Position = UDim2.fromOffset(0, 36)
Frame5.Parent = Frame
Frame5.BackgroundColor3 = Color3.fromRGB(18, 18, 22)
Frame5.BorderSizePixel = 0
Frame5.Size = UDim2.new(0, 120, 1, -46)
local UIListLayout = Instance.new("UIListLayout")
UIListLayout.Parent = Frame5
UIListLayout.Padding = UDim.new(0, 4)
UIListLayout.SortOrder = Enum.SortOrder.LayoutOrder
local UIPadding = Instance.new("UIPadding")
UIPadding.PaddingTop = UDim.new(0, 8)
UIPadding.PaddingBottom = UDim.new(0, 8)
UIPadding.Parent = Frame5
UIPadding.PaddingRight = UDim.new(0, 8)
UIPadding.PaddingLeft = UDim.new(0, 8)
local Frame6 = Instance.new("Frame")
Frame6.ClipsDescendants = true
Frame6.Name = "Content"
Frame6.Position = UDim2.fromOffset(126, 40)
Frame6.Parent = Frame
Frame6.BackgroundColor3 = Color3.fromRGB(18, 18, 22)
Frame6.BorderSizePixel = 0
Frame6.Size = UDim2.new(1, -130, 1, -46)
Frame2.InputBegan:Connect(function(input, gameProcessed)
end)
UserInputService.InputChanged:Connect(function(input2, gameProcessed2)
end)
UserInputService.InputEnded:Connect(function(input3, gameProcessed3)
end)
Players.LocalPlayer.CharacterAdded:Connect(function(character)
	task.wait(0.5)
	local Humanoid2 = Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
	Humanoid2.WalkSpeed = 16
	Humanoid2.JumpPower = 50
	Humanoid2.UseJumpPower = true
end)
RunService.Stepped:Connect(function(time, deltaTime)
end)
UserInputService.JumpRequest:Connect(function(arg3)
end)
task.spawn(function(...)
	task.wait(0.5)
	task.wait(0.5)
	task.wait(0.5)
	task.wait(0.5)
	task.wait(0.5)
	task.wait(0.5)
	task.wait(0.5)
	task.wait(0.5)
	task.wait(0.5)
end)
RunService.RenderStepped:Connect(function(deltaTime2)
end)
Players.PlayerAdded:Connect(function(player)
end)
Players.PlayerRemoving:Connect(function(player2)
end)
RunService.RenderStepped:Connect(function(deltaTime3)
end)
task.spawn(function(...)
	task.wait(0.08)
	task.wait(0.08)
	task.wait(0.08)
	task.wait(0.08)
	task.wait(0.08)
	task.wait(0.08)
	task.wait(0.08)
	task.wait(0.08)
	task.wait(0.08)
end)
RunService.RenderStepped:Connect(function(deltaTime4)
end)
local changedSignal = workspace:GetPropertyChangedSignal("CurrentCamera")
changedSignal:Connect(function(arg4)
	workspace.CurrentCamera.FieldOfView = 70
end)
local ScrollingFrame = Instance.new("ScrollingFrame")
ScrollingFrame.ScrollBarImageColor3 = Color3.fromRGB(90, 65, 165)
ScrollingFrame.AutomaticCanvasSize = Enum.AutomaticSize.Y
ScrollingFrame.ScrollBarThickness = 3
ScrollingFrame.Parent = Frame6
ScrollingFrame.Name = "Player"
ScrollingFrame.Visible = false
ScrollingFrame.BackgroundTransparency = 1
ScrollingFrame.CanvasSize = UDim2.new(0, 0, 0, 0)
ScrollingFrame.BorderSizePixel = 0
ScrollingFrame.Size = UDim2.fromScale(1, 1)
local UIListLayout2 = Instance.new("UIListLayout")
UIListLayout2.Parent = ScrollingFrame
UIListLayout2.Padding = UDim.new(0, 8)
UIListLayout2.SortOrder = Enum.SortOrder.LayoutOrder
local UIPadding2 = Instance.new("UIPadding")
UIPadding2.PaddingTop = UDim.new(0, 6)
UIPadding2.PaddingBottom = UDim.new(0, 6)
UIPadding2.Parent = ScrollingFrame
UIPadding2.PaddingRight = UDim.new(0, 6)
UIPadding2.PaddingLeft = UDim.new(0, 6)
local TextLabel2 = Instance.new("TextLabel")
TextLabel2.LayoutOrder = 1
TextLabel2.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel2.Parent = ScrollingFrame
TextLabel2.Text = "MOVEMENT"
TextLabel2.Font = Enum.Font.GothamBold
TextLabel2.BackgroundTransparency = 1
TextLabel2.TextXAlignment = Enum.TextXAlignment.Left
TextLabel2.TextSize = 10
TextLabel2.Size = UDim2.new(1, 0, 0, 18)
local Frame7 = Instance.new("Frame")
Frame7.LayoutOrder = 2
Frame7.Parent = ScrollingFrame
Frame7.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame7.BorderSizePixel = 0
Frame7.Size = UDim2.new(1, -8, 0, 46)
local UICorner5 = Instance.new("UICorner")
UICorner5.Parent = Frame7
UICorner5.CornerRadius = UDim.new(0, 6)
local TextLabel3 = Instance.new("TextLabel")
TextLabel3.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel3.Parent = Frame7
TextLabel3.Text = "Walk Speed"
TextLabel3.Font = Enum.Font.Gotham
TextLabel3.BackgroundTransparency = 1
TextLabel3.Position = UDim2.fromOffset(12, 6)
TextLabel3.TextXAlignment = Enum.TextXAlignment.Left
TextLabel3.TextSize = 12
TextLabel3.Size = UDim2.new(1, -70, 0, 20)
local TextLabel4 = Instance.new("TextLabel")
TextLabel4.TextColor3 = Color3.fromRGB(140, 100, 255)
TextLabel4.Parent = Frame7
TextLabel4.Text = "16"
TextLabel4.Font = Enum.Font.GothamBold
TextLabel4.BackgroundTransparency = 1
TextLabel4.Position = UDim2.new(1, -70, 0, 6)
TextLabel4.TextXAlignment = Enum.TextXAlignment.Right
TextLabel4.TextSize = 12
TextLabel4.Size = UDim2.fromOffset(58, 20)
local Frame8 = Instance.new("Frame")
Frame8.Position = UDim2.new(0, 12, 1, -16)
Frame8.Parent = Frame7
Frame8.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame8.BorderSizePixel = 0
Frame8.Size = UDim2.new(1, -24, 0, 6)
local UICorner6 = Instance.new("UICorner")
UICorner6.Parent = Frame8
UICorner6.CornerRadius = UDim.new(0, 3)
local Frame9 = Instance.new("Frame")
Frame9.Parent = Frame8
Frame9.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame9.BorderSizePixel = 0
Frame9.Size = UDim2.new(0, 0, 1, 0)
local UICorner7 = Instance.new("UICorner")
UICorner7.Parent = Frame9
UICorner7.CornerRadius = UDim.new(0, 3)
Frame9.Size = UDim2.new(0, 0, 1, 0)
TextLabel4.Text = "16"
local TextButton2 = Instance.new("TextButton")
TextButton2.Parent = Frame8
TextButton2.Text = ""
TextButton2.BackgroundTransparency = 1
TextButton2.Size = UDim2.new(1, 0, 1, 0)
TextButton2.InputBegan:Connect(function(input4, gameProcessed4)
end)
UserInputService.InputChanged:Connect(function(input5, gameProcessed5)
end)
UserInputService.InputEnded:Connect(function(input6, gameProcessed6)
end)
local Frame10 = Instance.new("Frame")
Frame10.LayoutOrder = 3
Frame10.Parent = ScrollingFrame
Frame10.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame10.BorderSizePixel = 0
Frame10.Size = UDim2.new(1, -8, 0, 46)
local UICorner8 = Instance.new("UICorner")
UICorner8.Parent = Frame10
UICorner8.CornerRadius = UDim.new(0, 6)
local TextLabel5 = Instance.new("TextLabel")
TextLabel5.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel5.Parent = Frame10
TextLabel5.Text = "Jump Power"
TextLabel5.Font = Enum.Font.Gotham
TextLabel5.BackgroundTransparency = 1
TextLabel5.Position = UDim2.fromOffset(12, 6)
TextLabel5.TextXAlignment = Enum.TextXAlignment.Left
TextLabel5.TextSize = 12
TextLabel5.Size = UDim2.new(1, -70, 0, 20)
local TextLabel6 = Instance.new("TextLabel")
TextLabel6.TextColor3 = Color3.fromRGB(140, 100, 255)
TextLabel6.Parent = Frame10
TextLabel6.Text = "50"
TextLabel6.Font = Enum.Font.GothamBold
TextLabel6.BackgroundTransparency = 1
TextLabel6.Position = UDim2.new(1, -70, 0, 6)
TextLabel6.TextXAlignment = Enum.TextXAlignment.Right
TextLabel6.TextSize = 12
TextLabel6.Size = UDim2.fromOffset(58, 20)
local Frame11 = Instance.new("Frame")
Frame11.Position = UDim2.new(0, 12, 1, -16)
Frame11.Parent = Frame10
Frame11.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame11.BorderSizePixel = 0
Frame11.Size = UDim2.new(1, -24, 0, 6)
local UICorner9 = Instance.new("UICorner")
UICorner9.Parent = Frame11
UICorner9.CornerRadius = UDim.new(0, 3)
local Frame12 = Instance.new("Frame")
Frame12.Parent = Frame11
Frame12.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame12.BorderSizePixel = 0
Frame12.Size = UDim2.new(0, 0, 1, 0)
local UICorner10 = Instance.new("UICorner")
UICorner10.Parent = Frame12
UICorner10.CornerRadius = UDim.new(0, 3)
Frame12.Size = UDim2.new(0, 0, 1, 0)
TextLabel6.Text = "50"
local TextButton3 = Instance.new("TextButton")
TextButton3.Parent = Frame11
TextButton3.Text = ""
TextButton3.BackgroundTransparency = 1
TextButton3.Size = UDim2.new(1, 0, 1, 0)
TextButton3.InputBegan:Connect(function(input7, gameProcessed7)
end)
UserInputService.InputChanged:Connect(function(input8, gameProcessed8)
end)
UserInputService.InputEnded:Connect(function(input9, gameProcessed9)
end)
local TextLabel7 = Instance.new("TextLabel")
TextLabel7.LayoutOrder = 4
TextLabel7.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel7.Parent = ScrollingFrame
TextLabel7.Text = "SURVIVAL"
TextLabel7.Font = Enum.Font.GothamBold
TextLabel7.BackgroundTransparency = 1
TextLabel7.TextXAlignment = Enum.TextXAlignment.Left
TextLabel7.TextSize = 10
TextLabel7.Size = UDim2.new(1, 0, 0, 18)
local Frame13 = Instance.new("Frame")
Frame13.LayoutOrder = 5
Frame13.Parent = ScrollingFrame
Frame13.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame13.BorderSizePixel = 0
Frame13.Size = UDim2.new(1, -8, 0, 32)
local UICorner11 = Instance.new("UICorner")
UICorner11.Parent = Frame13
UICorner11.CornerRadius = UDim.new(0, 6)
local TextLabel8 = Instance.new("TextLabel")
TextLabel8.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel8.Parent = Frame13
TextLabel8.Text = "Godmode"
TextLabel8.Font = Enum.Font.Gotham
TextLabel8.BackgroundTransparency = 1
TextLabel8.Position = UDim2.fromOffset(12, 0)
TextLabel8.TextXAlignment = Enum.TextXAlignment.Left
TextLabel8.TextSize = 12
TextLabel8.Size = UDim2.new(1, -60, 1, 0)
local Frame14 = Instance.new("Frame")
Frame14.Position = UDim2.new(1, -50, 0.5, -10)
Frame14.Parent = Frame13
Frame14.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame14.BorderSizePixel = 0
Frame14.Size = UDim2.fromOffset(40, 20)
local UICorner12 = Instance.new("UICorner")
UICorner12.Parent = Frame14
UICorner12.CornerRadius = UDim.new(0, 10)
local Frame15 = Instance.new("Frame")
Frame15.Position = UDim2.fromOffset(2, 2)
Frame15.Parent = Frame14
Frame15.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame15.BorderSizePixel = 0
Frame15.Size = UDim2.fromOffset(16, 16)
local UICorner13 = Instance.new("UICorner")
UICorner13.Parent = Frame15
UICorner13.CornerRadius = UDim.new(0, 8)
local TextButton4 = Instance.new("TextButton")
TextButton4.Parent = Frame13
TextButton4.Text = ""
TextButton4.BackgroundTransparency = 1
TextButton4.Size = UDim2.fromScale(1, 1)
TextButton4.MouseButton1Click:Connect(function()
	local tween6 = TweenService:Create(Frame14, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween6:Play()
	local tween7 = TweenService:Create(Frame15, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween7:Play()
	local Humanoid3 = Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
	Humanoid3.MaxHealth = math.huge
	Humanoid3.Health = math.huge
end)
local Frame16 = Instance.new("Frame")
Frame16.LayoutOrder = 6
Frame16.Parent = ScrollingFrame
Frame16.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame16.BorderSizePixel = 0
Frame16.Size = UDim2.new(1, -8, 0, 32)
local UICorner14 = Instance.new("UICorner")
UICorner14.Parent = Frame16
UICorner14.CornerRadius = UDim.new(0, 6)
local TextLabel9 = Instance.new("TextLabel")
TextLabel9.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel9.Parent = Frame16
TextLabel9.Text = "Auto Regen"
TextLabel9.Font = Enum.Font.Gotham
TextLabel9.BackgroundTransparency = 1
TextLabel9.Position = UDim2.fromOffset(12, 0)
TextLabel9.TextXAlignment = Enum.TextXAlignment.Left
TextLabel9.TextSize = 12
TextLabel9.Size = UDim2.new(1, -60, 1, 0)
local Frame17 = Instance.new("Frame")
Frame17.Position = UDim2.new(1, -50, 0.5, -10)
Frame17.Parent = Frame16
Frame17.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame17.BorderSizePixel = 0
Frame17.Size = UDim2.fromOffset(40, 20)
local UICorner15 = Instance.new("UICorner")
UICorner15.Parent = Frame17
UICorner15.CornerRadius = UDim.new(0, 10)
local Frame18 = Instance.new("Frame")
Frame18.Position = UDim2.fromOffset(2, 2)
Frame18.Parent = Frame17
Frame18.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame18.BorderSizePixel = 0
Frame18.Size = UDim2.fromOffset(16, 16)
local UICorner16 = Instance.new("UICorner")
UICorner16.Parent = Frame18
UICorner16.CornerRadius = UDim.new(0, 8)
local TextButton5 = Instance.new("TextButton")
TextButton5.Parent = Frame16
TextButton5.Text = ""
TextButton5.BackgroundTransparency = 1
TextButton5.Size = UDim2.fromScale(1, 1)
TextButton5.MouseButton1Click:Connect(function()
	local tween8 = TweenService:Create(Frame17, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween8:Play()
	local tween9 = TweenService:Create(Frame18, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween9:Play()
end)
local Frame19 = Instance.new("Frame")
Frame19.LayoutOrder = 7
Frame19.Parent = ScrollingFrame
Frame19.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame19.BorderSizePixel = 0
Frame19.Size = UDim2.new(1, -8, 0, 32)
local UICorner17 = Instance.new("UICorner")
UICorner17.Parent = Frame19
UICorner17.CornerRadius = UDim.new(0, 6)
local TextLabel10 = Instance.new("TextLabel")
TextLabel10.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel10.Parent = Frame19
TextLabel10.Text = "Infinite Jump"
TextLabel10.Font = Enum.Font.Gotham
TextLabel10.BackgroundTransparency = 1
TextLabel10.Position = UDim2.fromOffset(12, 0)
TextLabel10.TextXAlignment = Enum.TextXAlignment.Left
TextLabel10.TextSize = 12
TextLabel10.Size = UDim2.new(1, -60, 1, 0)
local Frame20 = Instance.new("Frame")
Frame20.Position = UDim2.new(1, -50, 0.5, -10)
Frame20.Parent = Frame19
Frame20.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame20.BorderSizePixel = 0
Frame20.Size = UDim2.fromOffset(40, 20)
local UICorner18 = Instance.new("UICorner")
UICorner18.Parent = Frame20
UICorner18.CornerRadius = UDim.new(0, 10)
local Frame21 = Instance.new("Frame")
Frame21.Position = UDim2.fromOffset(2, 2)
Frame21.Parent = Frame20
Frame21.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame21.BorderSizePixel = 0
Frame21.Size = UDim2.fromOffset(16, 16)
local UICorner19 = Instance.new("UICorner")
UICorner19.Parent = Frame21
UICorner19.CornerRadius = UDim.new(0, 8)
local TextButton6 = Instance.new("TextButton")
TextButton6.Parent = Frame19
TextButton6.Text = ""
TextButton6.BackgroundTransparency = 1
TextButton6.Size = UDim2.fromScale(1, 1)
TextButton6.MouseButton1Click:Connect(function()
	local tween10 = TweenService:Create(Frame20, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween10:Play()
	local tween11 = TweenService:Create(Frame21, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween11:Play()
end)
local ScrollingFrame2 = Instance.new("ScrollingFrame")
ScrollingFrame2.ScrollBarImageColor3 = Color3.fromRGB(90, 65, 165)
ScrollingFrame2.AutomaticCanvasSize = Enum.AutomaticSize.Y
ScrollingFrame2.ScrollBarThickness = 3
ScrollingFrame2.Parent = Frame6
ScrollingFrame2.Name = "Visual"
ScrollingFrame2.Visible = false
ScrollingFrame2.BackgroundTransparency = 1
ScrollingFrame2.CanvasSize = UDim2.new(0, 0, 0, 0)
ScrollingFrame2.BorderSizePixel = 0
ScrollingFrame2.Size = UDim2.fromScale(1, 1)
local UIListLayout3 = Instance.new("UIListLayout")
UIListLayout3.Parent = ScrollingFrame2
UIListLayout3.Padding = UDim.new(0, 8)
UIListLayout3.SortOrder = Enum.SortOrder.LayoutOrder
local UIPadding3 = Instance.new("UIPadding")
UIPadding3.PaddingTop = UDim.new(0, 6)
UIPadding3.PaddingBottom = UDim.new(0, 6)
UIPadding3.Parent = ScrollingFrame2
UIPadding3.PaddingRight = UDim.new(0, 6)
UIPadding3.PaddingLeft = UDim.new(0, 6)
local TextLabel11 = Instance.new("TextLabel")
TextLabel11.LayoutOrder = 1
TextLabel11.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel11.Parent = ScrollingFrame2
TextLabel11.Text = "LIGHTING"
TextLabel11.Font = Enum.Font.GothamBold
TextLabel11.BackgroundTransparency = 1
TextLabel11.TextXAlignment = Enum.TextXAlignment.Left
TextLabel11.TextSize = 10
TextLabel11.Size = UDim2.new(1, 0, 0, 18)
local Frame22 = Instance.new("Frame")
Frame22.LayoutOrder = 2
Frame22.Parent = ScrollingFrame2
Frame22.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame22.BorderSizePixel = 0
Frame22.Size = UDim2.new(1, -8, 0, 32)
local UICorner20 = Instance.new("UICorner")
UICorner20.Parent = Frame22
UICorner20.CornerRadius = UDim.new(0, 6)
local TextLabel12 = Instance.new("TextLabel")
TextLabel12.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel12.Parent = Frame22
TextLabel12.Text = "Fullbright"
TextLabel12.Font = Enum.Font.Gotham
TextLabel12.BackgroundTransparency = 1
TextLabel12.Position = UDim2.fromOffset(12, 0)
TextLabel12.TextXAlignment = Enum.TextXAlignment.Left
TextLabel12.TextSize = 12
TextLabel12.Size = UDim2.new(1, -60, 1, 0)
local Frame23 = Instance.new("Frame")
Frame23.Position = UDim2.new(1, -50, 0.5, -10)
Frame23.Parent = Frame22
Frame23.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame23.BorderSizePixel = 0
Frame23.Size = UDim2.fromOffset(40, 20)
local UICorner21 = Instance.new("UICorner")
UICorner21.Parent = Frame23
UICorner21.CornerRadius = UDim.new(0, 10)
local Frame24 = Instance.new("Frame")
Frame24.Position = UDim2.fromOffset(2, 2)
Frame24.Parent = Frame23
Frame24.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame24.BorderSizePixel = 0
Frame24.Size = UDim2.fromOffset(16, 16)
local UICorner22 = Instance.new("UICorner")
UICorner22.Parent = Frame24
UICorner22.CornerRadius = UDim.new(0, 8)
local TextButton7 = Instance.new("TextButton")
TextButton7.Parent = Frame22
TextButton7.Text = ""
TextButton7.BackgroundTransparency = 1
TextButton7.Size = UDim2.fromScale(1, 1)
TextButton7.MouseButton1Click:Connect(function()
	local tween12 = TweenService:Create(Frame23, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween12:Play()
	local tween13 = TweenService:Create(Frame24, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween13:Play()
	Lighting.Brightness = 2
	Lighting.Ambient = Color3.fromRGB(178, 178, 178)
	Lighting.OutdoorAmbient = Color3.fromRGB(178, 178, 178)
	Lighting.ClockTime = 12
	Lighting.GlobalShadows = false
end)
local Frame25 = Instance.new("Frame")
Frame25.LayoutOrder = 3
Frame25.Parent = ScrollingFrame2
Frame25.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame25.BorderSizePixel = 0
Frame25.Size = UDim2.new(1, -8, 0, 32)
local UICorner23 = Instance.new("UICorner")
UICorner23.Parent = Frame25
UICorner23.CornerRadius = UDim.new(0, 6)
local TextLabel13 = Instance.new("TextLabel")
TextLabel13.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel13.Parent = Frame25
TextLabel13.Text = "Remove Fog"
TextLabel13.Font = Enum.Font.Gotham
TextLabel13.BackgroundTransparency = 1
TextLabel13.Position = UDim2.fromOffset(12, 0)
TextLabel13.TextXAlignment = Enum.TextXAlignment.Left
TextLabel13.TextSize = 12
TextLabel13.Size = UDim2.new(1, -60, 1, 0)
local Frame26 = Instance.new("Frame")
Frame26.Position = UDim2.new(1, -50, 0.5, -10)
Frame26.Parent = Frame25
Frame26.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame26.BorderSizePixel = 0
Frame26.Size = UDim2.fromOffset(40, 20)
local UICorner24 = Instance.new("UICorner")
UICorner24.Parent = Frame26
UICorner24.CornerRadius = UDim.new(0, 10)
local Frame27 = Instance.new("Frame")
Frame27.Position = UDim2.fromOffset(2, 2)
Frame27.Parent = Frame26
Frame27.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame27.BorderSizePixel = 0
Frame27.Size = UDim2.fromOffset(16, 16)
local UICorner25 = Instance.new("UICorner")
UICorner25.Parent = Frame27
UICorner25.CornerRadius = UDim.new(0, 8)
local TextButton8 = Instance.new("TextButton")
TextButton8.Parent = Frame25
TextButton8.Text = ""
TextButton8.BackgroundTransparency = 1
TextButton8.Size = UDim2.fromScale(1, 1)
TextButton8.MouseButton1Click:Connect(function()
	local tween14 = TweenService:Create(Frame26, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween14:Play()
	local tween15 = TweenService:Create(Frame27, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween15:Play()
	Lighting.Brightness = 2
	Lighting.Ambient = Color3.fromRGB(178, 178, 178)
	Lighting.OutdoorAmbient = Color3.fromRGB(178, 178, 178)
	Lighting.ClockTime = 12
	Lighting.GlobalShadows = false
	Lighting.FogEnd = 1000000
	Lighting.FogStart = 0
end)
local TextLabel14 = Instance.new("TextLabel")
TextLabel14.LayoutOrder = 4
TextLabel14.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel14.Parent = ScrollingFrame2
TextLabel14.Text = "PLAYERS"
TextLabel14.Font = Enum.Font.GothamBold
TextLabel14.BackgroundTransparency = 1
TextLabel14.TextXAlignment = Enum.TextXAlignment.Left
TextLabel14.TextSize = 10
TextLabel14.Size = UDim2.new(1, 0, 0, 18)
local Frame28 = Instance.new("Frame")
Frame28.LayoutOrder = 5
Frame28.Parent = ScrollingFrame2
Frame28.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame28.BorderSizePixel = 0
Frame28.Size = UDim2.new(1, -8, 0, 32)
local UICorner26 = Instance.new("UICorner")
UICorner26.Parent = Frame28
UICorner26.CornerRadius = UDim.new(0, 6)
local TextLabel15 = Instance.new("TextLabel")
TextLabel15.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel15.Parent = Frame28
TextLabel15.Text = "ESP Highlights"
TextLabel15.Font = Enum.Font.Gotham
TextLabel15.BackgroundTransparency = 1
TextLabel15.Position = UDim2.fromOffset(12, 0)
TextLabel15.TextXAlignment = Enum.TextXAlignment.Left
TextLabel15.TextSize = 12
TextLabel15.Size = UDim2.new(1, -60, 1, 0)
local Frame29 = Instance.new("Frame")
Frame29.Position = UDim2.new(1, -50, 0.5, -10)
Frame29.Parent = Frame28
Frame29.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame29.BorderSizePixel = 0
Frame29.Size = UDim2.fromOffset(40, 20)
local UICorner27 = Instance.new("UICorner")
UICorner27.Parent = Frame29
UICorner27.CornerRadius = UDim.new(0, 10)
local Frame30 = Instance.new("Frame")
Frame30.Position = UDim2.fromOffset(2, 2)
Frame30.Parent = Frame29
Frame30.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame30.BorderSizePixel = 0
Frame30.Size = UDim2.fromOffset(16, 16)
local UICorner28 = Instance.new("UICorner")
UICorner28.Parent = Frame30
UICorner28.CornerRadius = UDim.new(0, 8)
local TextButton9 = Instance.new("TextButton")
TextButton9.Parent = Frame28
TextButton9.Text = ""
TextButton9.BackgroundTransparency = 1
TextButton9.Size = UDim2.fromScale(1, 1)
TextButton9.MouseButton1Click:Connect(function()
	local tween16 = TweenService:Create(Frame29, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween16:Play()
	local tween17 = TweenService:Create(Frame30, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween17:Play()
	local players2 = Players:GetPlayers()
	for i2, v2 in ipairs(players2) do
		local Highlight = Instance.new("Highlight")
		Highlight.FillColor = Color3.fromRGB(140, 100, 255)
		Highlight.Name = "RT_ESP"
		Highlight.OutlineColor = Color3.fromRGB(200, 170, 255)
		Highlight.Parent = hui
		Highlight.FillTransparency = 0.7
		Highlight.OutlineTransparency = 0
	end
end)
local TextLabel16 = Instance.new("TextLabel")
TextLabel16.LayoutOrder = 6
TextLabel16.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel16.Parent = ScrollingFrame2
TextLabel16.Text = "CAMERA"
TextLabel16.Font = Enum.Font.GothamBold
TextLabel16.BackgroundTransparency = 1
TextLabel16.TextXAlignment = Enum.TextXAlignment.Left
TextLabel16.TextSize = 10
TextLabel16.Size = UDim2.new(1, 0, 0, 18)
local Frame31 = Instance.new("Frame")
Frame31.LayoutOrder = 7
Frame31.Parent = ScrollingFrame2
Frame31.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame31.BorderSizePixel = 0
Frame31.Size = UDim2.new(1, -8, 0, 46)
local UICorner29 = Instance.new("UICorner")
UICorner29.Parent = Frame31
UICorner29.CornerRadius = UDim.new(0, 6)
local TextLabel17 = Instance.new("TextLabel")
TextLabel17.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel17.Parent = Frame31
TextLabel17.Text = "Field of View"
TextLabel17.Font = Enum.Font.Gotham
TextLabel17.BackgroundTransparency = 1
TextLabel17.Position = UDim2.fromOffset(12, 6)
TextLabel17.TextXAlignment = Enum.TextXAlignment.Left
TextLabel17.TextSize = 12
TextLabel17.Size = UDim2.new(1, -70, 0, 20)
local TextLabel18 = Instance.new("TextLabel")
TextLabel18.TextColor3 = Color3.fromRGB(140, 100, 255)
TextLabel18.Parent = Frame31
TextLabel18.Text = "70"
TextLabel18.Font = Enum.Font.GothamBold
TextLabel18.BackgroundTransparency = 1
TextLabel18.Position = UDim2.new(1, -70, 0, 6)
TextLabel18.TextXAlignment = Enum.TextXAlignment.Right
TextLabel18.TextSize = 12
TextLabel18.Size = UDim2.fromOffset(58, 20)
local Frame32 = Instance.new("Frame")
Frame32.Position = UDim2.new(0, 12, 1, -16)
Frame32.Parent = Frame31
Frame32.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame32.BorderSizePixel = 0
Frame32.Size = UDim2.new(1, -24, 0, 6)
local UICorner30 = Instance.new("UICorner")
UICorner30.Parent = Frame32
UICorner30.CornerRadius = UDim.new(0, 3)
local Frame33 = Instance.new("Frame")
Frame33.Parent = Frame32
Frame33.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame33.BorderSizePixel = 0
Frame33.Size = UDim2.new(0, 0, 1, 0)
local UICorner31 = Instance.new("UICorner")
UICorner31.Parent = Frame33
UICorner31.CornerRadius = UDim.new(0, 3)
Frame33.Size = UDim2.new(0.44444444444444442, 0, 1, 0)
TextLabel18.Text = "70"
local TextButton10 = Instance.new("TextButton")
TextButton10.Parent = Frame32
TextButton10.Text = ""
TextButton10.BackgroundTransparency = 1
TextButton10.Size = UDim2.new(1, 0, 1, 0)
TextButton10.InputBegan:Connect(function(input10, gameProcessed10)
end)
UserInputService.InputChanged:Connect(function(input11, gameProcessed11)
end)
UserInputService.InputEnded:Connect(function(input12, gameProcessed12)
end)
local ScrollingFrame3 = Instance.new("ScrollingFrame")
ScrollingFrame3.ScrollBarImageColor3 = Color3.fromRGB(90, 65, 165)
ScrollingFrame3.AutomaticCanvasSize = Enum.AutomaticSize.Y
ScrollingFrame3.ScrollBarThickness = 3
ScrollingFrame3.Parent = Frame6
ScrollingFrame3.Name = "Movement"
ScrollingFrame3.Visible = false
ScrollingFrame3.BackgroundTransparency = 1
ScrollingFrame3.CanvasSize = UDim2.new(0, 0, 0, 0)
ScrollingFrame3.BorderSizePixel = 0
ScrollingFrame3.Size = UDim2.fromScale(1, 1)
local UIListLayout4 = Instance.new("UIListLayout")
UIListLayout4.Parent = ScrollingFrame3
UIListLayout4.Padding = UDim.new(0, 8)
UIListLayout4.SortOrder = Enum.SortOrder.LayoutOrder
local UIPadding4 = Instance.new("UIPadding")
UIPadding4.PaddingTop = UDim.new(0, 6)
UIPadding4.PaddingBottom = UDim.new(0, 6)
UIPadding4.Parent = ScrollingFrame3
UIPadding4.PaddingRight = UDim.new(0, 6)
UIPadding4.PaddingLeft = UDim.new(0, 6)
local TextLabel19 = Instance.new("TextLabel")
TextLabel19.LayoutOrder = 1
TextLabel19.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel19.Parent = ScrollingFrame3
TextLabel19.Text = "FLIGHT"
TextLabel19.Font = Enum.Font.GothamBold
TextLabel19.BackgroundTransparency = 1
TextLabel19.TextXAlignment = Enum.TextXAlignment.Left
TextLabel19.TextSize = 10
TextLabel19.Size = UDim2.new(1, 0, 0, 18)
local Frame34 = Instance.new("Frame")
Frame34.LayoutOrder = 2
Frame34.Parent = ScrollingFrame3
Frame34.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame34.BorderSizePixel = 0
Frame34.Size = UDim2.new(1, -8, 0, 32)
local UICorner32 = Instance.new("UICorner")
UICorner32.Parent = Frame34
UICorner32.CornerRadius = UDim.new(0, 6)
local TextLabel20 = Instance.new("TextLabel")
TextLabel20.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel20.Parent = Frame34
TextLabel20.Text = "Fly"
TextLabel20.Font = Enum.Font.Gotham
TextLabel20.BackgroundTransparency = 1
TextLabel20.Position = UDim2.fromOffset(12, 0)
TextLabel20.TextXAlignment = Enum.TextXAlignment.Left
TextLabel20.TextSize = 12
TextLabel20.Size = UDim2.new(1, -60, 1, 0)
local Frame35 = Instance.new("Frame")
Frame35.Position = UDim2.new(1, -50, 0.5, -10)
Frame35.Parent = Frame34
Frame35.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame35.BorderSizePixel = 0
Frame35.Size = UDim2.fromOffset(40, 20)
local UICorner33 = Instance.new("UICorner")
UICorner33.Parent = Frame35
UICorner33.CornerRadius = UDim.new(0, 10)
local Frame36 = Instance.new("Frame")
Frame36.Position = UDim2.fromOffset(2, 2)
Frame36.Parent = Frame35
Frame36.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame36.BorderSizePixel = 0
Frame36.Size = UDim2.fromOffset(16, 16)
local UICorner34 = Instance.new("UICorner")
UICorner34.Parent = Frame36
UICorner34.CornerRadius = UDim.new(0, 8)
local TextButton11 = Instance.new("TextButton")
TextButton11.Parent = Frame34
TextButton11.Text = ""
TextButton11.BackgroundTransparency = 1
TextButton11.Size = UDim2.fromScale(1, 1)
TextButton11.MouseButton1Click:Connect(function()
	local tween18 = TweenService:Create(Frame35, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween18:Play()
	local tween19 = TweenService:Create(Frame36, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween19:Play()
	local HumanoidRootPart = Players.LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
	local BodyVelocity = Instance.new("BodyVelocity")
	BodyVelocity.P = 1250
	BodyVelocity.Name = "RT_FlyVelocity"
	BodyVelocity.MaxForce = Vector3.new(100000, 100000, 100000)
	BodyVelocity.Parent = HumanoidRootPart
	BodyVelocity.Velocity = Vector3.new(0, 0, 0)
	local BodyGyro = Instance.new("BodyGyro")
	BodyGyro.P = 1250
	BodyGyro.Name = "RT_FlyGyro"
	BodyGyro.MaxTorque = Vector3.new(100000, 100000, 100000)
	BodyGyro.Parent = HumanoidRootPart
	BodyGyro.D = 50
	BodyGyro.CFrame = HumanoidRootPart.CFrame
end)
local Frame37 = Instance.new("Frame")
Frame37.LayoutOrder = 3
Frame37.Parent = ScrollingFrame3
Frame37.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame37.BorderSizePixel = 0
Frame37.Size = UDim2.new(1, -8, 0, 46)
local UICorner35 = Instance.new("UICorner")
UICorner35.Parent = Frame37
UICorner35.CornerRadius = UDim.new(0, 6)
local TextLabel21 = Instance.new("TextLabel")
TextLabel21.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel21.Parent = Frame37
TextLabel21.Text = "Fly Speed"
TextLabel21.Font = Enum.Font.Gotham
TextLabel21.BackgroundTransparency = 1
TextLabel21.Position = UDim2.fromOffset(12, 6)
TextLabel21.TextXAlignment = Enum.TextXAlignment.Left
TextLabel21.TextSize = 12
TextLabel21.Size = UDim2.new(1, -70, 0, 20)
local TextLabel22 = Instance.new("TextLabel")
TextLabel22.TextColor3 = Color3.fromRGB(140, 100, 255)
TextLabel22.Parent = Frame37
TextLabel22.Text = "60"
TextLabel22.Font = Enum.Font.GothamBold
TextLabel22.BackgroundTransparency = 1
TextLabel22.Position = UDim2.new(1, -70, 0, 6)
TextLabel22.TextXAlignment = Enum.TextXAlignment.Right
TextLabel22.TextSize = 12
TextLabel22.Size = UDim2.fromOffset(58, 20)
local Frame38 = Instance.new("Frame")
Frame38.Position = UDim2.new(0, 12, 1, -16)
Frame38.Parent = Frame37
Frame38.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame38.BorderSizePixel = 0
Frame38.Size = UDim2.new(1, -24, 0, 6)
local UICorner36 = Instance.new("UICorner")
UICorner36.Parent = Frame38
UICorner36.CornerRadius = UDim.new(0, 3)
local Frame39 = Instance.new("Frame")
Frame39.Parent = Frame38
Frame39.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame39.BorderSizePixel = 0
Frame39.Size = UDim2.new(0, 0, 1, 0)
local UICorner37 = Instance.new("UICorner")
UICorner37.Parent = Frame39
UICorner37.CornerRadius = UDim.new(0, 3)
Frame39.Size = UDim2.new(0.14285714285714285, 0, 1, 0)
TextLabel22.Text = "60"
local TextButton12 = Instance.new("TextButton")
TextButton12.Parent = Frame38
TextButton12.Text = ""
TextButton12.BackgroundTransparency = 1
TextButton12.Size = UDim2.new(1, 0, 1, 0)
TextButton12.InputBegan:Connect(function(input13, gameProcessed13)
end)
UserInputService.InputChanged:Connect(function(input14, gameProcessed14)
end)
UserInputService.InputEnded:Connect(function(input15, gameProcessed15)
end)
local TextLabel23 = Instance.new("TextLabel")
TextLabel23.LayoutOrder = 4
TextLabel23.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel23.Parent = ScrollingFrame3
TextLabel23.Text = "PHYSICS"
TextLabel23.Font = Enum.Font.GothamBold
TextLabel23.BackgroundTransparency = 1
TextLabel23.TextXAlignment = Enum.TextXAlignment.Left
TextLabel23.TextSize = 10
TextLabel23.Size = UDim2.new(1, 0, 0, 18)
local Frame40 = Instance.new("Frame")
Frame40.LayoutOrder = 5
Frame40.Parent = ScrollingFrame3
Frame40.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame40.BorderSizePixel = 0
Frame40.Size = UDim2.new(1, -8, 0, 32)
local UICorner38 = Instance.new("UICorner")
UICorner38.Parent = Frame40
UICorner38.CornerRadius = UDim.new(0, 6)
local TextLabel24 = Instance.new("TextLabel")
TextLabel24.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel24.Parent = Frame40
TextLabel24.Text = "Noclip"
TextLabel24.Font = Enum.Font.Gotham
TextLabel24.BackgroundTransparency = 1
TextLabel24.Position = UDim2.fromOffset(12, 0)
TextLabel24.TextXAlignment = Enum.TextXAlignment.Left
TextLabel24.TextSize = 12
TextLabel24.Size = UDim2.new(1, -60, 1, 0)
local Frame41 = Instance.new("Frame")
Frame41.Position = UDim2.new(1, -50, 0.5, -10)
Frame41.Parent = Frame40
Frame41.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame41.BorderSizePixel = 0
Frame41.Size = UDim2.fromOffset(40, 20)
local UICorner39 = Instance.new("UICorner")
UICorner39.Parent = Frame41
UICorner39.CornerRadius = UDim.new(0, 10)
local Frame42 = Instance.new("Frame")
Frame42.Position = UDim2.fromOffset(2, 2)
Frame42.Parent = Frame41
Frame42.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame42.BorderSizePixel = 0
Frame42.Size = UDim2.fromOffset(16, 16)
local UICorner40 = Instance.new("UICorner")
UICorner40.Parent = Frame42
UICorner40.CornerRadius = UDim.new(0, 8)
local TextButton13 = Instance.new("TextButton")
TextButton13.Parent = Frame40
TextButton13.Text = ""
TextButton13.BackgroundTransparency = 1
TextButton13.Size = UDim2.fromScale(1, 1)
TextButton13.MouseButton1Click:Connect(function()
	local tween20 = TweenService:Create(Frame41, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween20:Play()
	local tween21 = TweenService:Create(Frame42, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween21:Play()
end)
local Frame43 = Instance.new("Frame")
Frame43.LayoutOrder = 6
Frame43.Parent = ScrollingFrame3
Frame43.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame43.BorderSizePixel = 0
Frame43.Size = UDim2.new(1, -8, 0, 32)
local UICorner41 = Instance.new("UICorner")
UICorner41.Parent = Frame43
UICorner41.CornerRadius = UDim.new(0, 6)
local TextLabel25 = Instance.new("TextLabel")
TextLabel25.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel25.Parent = Frame43
TextLabel25.Text = "Flip Gravity"
TextLabel25.Font = Enum.Font.Gotham
TextLabel25.BackgroundTransparency = 1
TextLabel25.Position = UDim2.fromOffset(12, 0)
TextLabel25.TextXAlignment = Enum.TextXAlignment.Left
TextLabel25.TextSize = 12
TextLabel25.Size = UDim2.new(1, -60, 1, 0)
local Frame44 = Instance.new("Frame")
Frame44.Position = UDim2.new(1, -50, 0.5, -10)
Frame44.Parent = Frame43
Frame44.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame44.BorderSizePixel = 0
Frame44.Size = UDim2.fromOffset(40, 20)
local UICorner42 = Instance.new("UICorner")
UICorner42.Parent = Frame44
UICorner42.CornerRadius = UDim.new(0, 10)
local Frame45 = Instance.new("Frame")
Frame45.Position = UDim2.fromOffset(2, 2)
Frame45.Parent = Frame44
Frame45.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame45.BorderSizePixel = 0
Frame45.Size = UDim2.fromOffset(16, 16)
local UICorner43 = Instance.new("UICorner")
UICorner43.Parent = Frame45
UICorner43.CornerRadius = UDim.new(0, 8)
local TextButton14 = Instance.new("TextButton")
TextButton14.Parent = Frame43
TextButton14.Text = ""
TextButton14.BackgroundTransparency = 1
TextButton14.Size = UDim2.fromScale(1, 1)
TextButton14.MouseButton1Click:Connect(function()
	local tween22 = TweenService:Create(Frame44, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween22:Play()
	local tween23 = TweenService:Create(Frame45, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween23:Play()
	workspace.Gravity = -196.2
end)
local TextButton15 = Instance.new("TextButton")
TextButton15.LayoutOrder = 7
TextButton15.TextColor3 = Color3.fromRGB(235, 235, 240)
TextButton15.Parent = ScrollingFrame3
TextButton15.Text = "Reset Character"
TextButton15.AutoButtonColor = false
TextButton15.Font = Enum.Font.GothamBold
TextButton15.BackgroundColor3 = Color3.fromRGB(230, 80, 100)
TextButton15.TextSize = 12
TextButton15.Size = UDim2.new(1, -8, 0, 30)
local UICorner44 = Instance.new("UICorner")
UICorner44.Parent = TextButton15
UICorner44.CornerRadius = UDim.new(0, 6)
TextButton15.MouseEnter:Connect(function(arg5)
	local tween24 = TweenService:Create(TextButton15, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(34, 34, 42) })
	tween24:Play()
end)
TextButton15.MouseLeave:Connect(function(arg6)
	local tween25 = TweenService:Create(TextButton15, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(230, 80, 100) })
	tween25:Play()
end)
TextButton15.MouseButton1Click:Connect(function()
	local Humanoid4 = Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
	Humanoid4.Health = 0
end)
local ScrollingFrame4 = Instance.new("ScrollingFrame")
ScrollingFrame4.ScrollBarImageColor3 = Color3.fromRGB(90, 65, 165)
ScrollingFrame4.AutomaticCanvasSize = Enum.AutomaticSize.Y
ScrollingFrame4.ScrollBarThickness = 3
ScrollingFrame4.Parent = Frame6
ScrollingFrame4.Name = "Teleport"
ScrollingFrame4.Visible = false
ScrollingFrame4.BackgroundTransparency = 1
ScrollingFrame4.CanvasSize = UDim2.new(0, 0, 0, 0)
ScrollingFrame4.BorderSizePixel = 0
ScrollingFrame4.Size = UDim2.fromScale(1, 1)
local UIListLayout5 = Instance.new("UIListLayout")
UIListLayout5.Parent = ScrollingFrame4
UIListLayout5.Padding = UDim.new(0, 8)
UIListLayout5.SortOrder = Enum.SortOrder.LayoutOrder
local UIPadding5 = Instance.new("UIPadding")
UIPadding5.PaddingTop = UDim.new(0, 6)
UIPadding5.PaddingBottom = UDim.new(0, 6)
UIPadding5.Parent = ScrollingFrame4
UIPadding5.PaddingRight = UDim.new(0, 6)
UIPadding5.PaddingLeft = UDim.new(0, 6)
local TextLabel26 = Instance.new("TextLabel")
TextLabel26.LayoutOrder = 1
TextLabel26.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel26.Parent = ScrollingFrame4
TextLabel26.Text = "PLAYERS"
TextLabel26.Font = Enum.Font.GothamBold
TextLabel26.BackgroundTransparency = 1
TextLabel26.TextXAlignment = Enum.TextXAlignment.Left
TextLabel26.TextSize = 10
TextLabel26.Size = UDim2.new(1, 0, 0, 18)
local Frame46 = Instance.new("Frame")
Frame46.LayoutOrder = 2
Frame46.Parent = ScrollingFrame4
Frame46.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame46.BorderSizePixel = 0
Frame46.Size = UDim2.new(1, -8, 0, 150)
local UICorner45 = Instance.new("UICorner")
UICorner45.Parent = Frame46
UICorner45.CornerRadius = UDim.new(0, 6)
local ScrollingFrame5 = Instance.new("ScrollingFrame")
ScrollingFrame5.ScrollBarImageColor3 = Color3.fromRGB(90, 65, 165)
ScrollingFrame5.Parent = Frame46
ScrollingFrame5.BackgroundTransparency = 1
ScrollingFrame5.CanvasSize = UDim2.new(0, 0, 0, 0)
ScrollingFrame5.AutomaticCanvasSize = Enum.AutomaticSize.Y
ScrollingFrame5.ScrollBarThickness = 3
ScrollingFrame5.BorderSizePixel = 0
ScrollingFrame5.Size = UDim2.fromScale(1, 1)
local UIListLayout6 = Instance.new("UIListLayout")
UIListLayout6.Parent = ScrollingFrame5
UIListLayout6.Padding = UDim.new(0, 4)
UIListLayout6.SortOrder = Enum.SortOrder.LayoutOrder
local UIPadding6 = Instance.new("UIPadding")
UIPadding6.PaddingTop = UDim.new(0, 6)
UIPadding6.PaddingBottom = UDim.new(0, 6)
UIPadding6.Parent = ScrollingFrame5
UIPadding6.PaddingRight = UDim.new(0, 6)
UIPadding6.PaddingLeft = UDim.new(0, 6)
ScrollingFrame5:GetChildren()
local players = Players:GetPlayers()
for i, v in ipairs(players) do
	local TextButton16 = Instance.new("TextButton")
	TextButton16.LayoutOrder = i
	TextButton16.TextColor3 = Color3.fromRGB(235, 235, 240)
	TextButton16.Parent = ScrollingFrame5
	TextButton16.Text = v.Name
	TextButton16.AutoButtonColor = false
	TextButton16.Font = Enum.Font.Gotham
	TextButton16.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
	TextButton16.TextSize = 11
	TextButton16.Size = UDim2.new(1, -4, 0, 26)
	local UICorner46 = Instance.new("UICorner")
	UICorner46.Parent = TextButton16
	UICorner46.CornerRadius = UDim.new(0, 5)
	TextButton16.MouseButton1Click:Connect(function()
		local HumanoidRootPart2 = Players.LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
		local HumanoidRootPart3 = v.Character:FindFirstChild("HumanoidRootPart")
		HumanoidRootPart2.CFrame = (HumanoidRootPart3.CFrame + Vector3.new(0, 3, 0))
	end)
end
Players.PlayerAdded:Connect(function(player3)
	ScrollingFrame5:GetChildren()
	local players3 = Players:GetPlayers()
	for i3, v3 in ipairs(players3) do
		local TextButton30 = Instance.new("TextButton")
		TextButton30.LayoutOrder = i3
		TextButton30.TextColor3 = Color3.fromRGB(235, 235, 240)
		TextButton30.Parent = ScrollingFrame5
		TextButton30.Text = v3.Name
		TextButton30.AutoButtonColor = false
		TextButton30.Font = Enum.Font.Gotham
		TextButton30.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
		TextButton30.TextSize = 11
		TextButton30.Size = UDim2.new(1, -4, 0, 26)
		local UICorner69 = Instance.new("UICorner")
		UICorner69.Parent = TextButton30
		UICorner69.CornerRadius = UDim.new(0, 5)
		TextButton30.MouseButton1Click:Connect(function()
			local HumanoidRootPart8 = Players.LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
			local HumanoidRootPart9 = v3.Character:FindFirstChild("HumanoidRootPart")
			HumanoidRootPart8.CFrame = (HumanoidRootPart9.CFrame + Vector3.new(0, 3, 0))
		end)
	end
end)
Players.PlayerRemoving:Connect(function(player4)
	task.wait(0.1)
	ScrollingFrame5:GetChildren()
	TextButton30:Destroy()
	local players4 = Players:GetPlayers()
	for i4, v4 in ipairs(players4) do
		local TextButton31 = Instance.new("TextButton")
		TextButton31.LayoutOrder = i4
		TextButton31.TextColor3 = Color3.fromRGB(235, 235, 240)
		TextButton31.Parent = ScrollingFrame5
		TextButton31.Text = v4.Name
		TextButton31.AutoButtonColor = false
		TextButton31.Font = Enum.Font.Gotham
		TextButton31.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
		TextButton31.TextSize = 11
		TextButton31.Size = UDim2.new(1, -4, 0, 26)
		local UICorner70 = Instance.new("UICorner")
		UICorner70.Parent = TextButton31
		UICorner70.CornerRadius = UDim.new(0, 5)
		TextButton31.MouseButton1Click:Connect(function()
			local HumanoidRootPart10 = Players.LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
			local HumanoidRootPart11 = v4.Character:FindFirstChild("HumanoidRootPart")
			HumanoidRootPart10.CFrame = (HumanoidRootPart11.CFrame + Vector3.new(0, 3, 0))
		end)
	end
end)
local TextLabel27 = Instance.new("TextLabel")
TextLabel27.LayoutOrder = 3
TextLabel27.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel27.Parent = ScrollingFrame4
TextLabel27.Text = "ACTIONS"
TextLabel27.Font = Enum.Font.GothamBold
TextLabel27.BackgroundTransparency = 1
TextLabel27.TextXAlignment = Enum.TextXAlignment.Left
TextLabel27.TextSize = 10
TextLabel27.Size = UDim2.new(1, 0, 0, 18)
local TextButton17 = Instance.new("TextButton")
TextButton17.LayoutOrder = 4
TextButton17.TextColor3 = Color3.fromRGB(235, 235, 240)
TextButton17.Parent = ScrollingFrame4
TextButton17.Text = "Teleport to Random Player"
TextButton17.AutoButtonColor = false
TextButton17.Font = Enum.Font.GothamBold
TextButton17.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
TextButton17.TextSize = 12
TextButton17.Size = UDim2.new(1, -8, 0, 30)
local UICorner47 = Instance.new("UICorner")
UICorner47.Parent = TextButton17
UICorner47.CornerRadius = UDim.new(0, 6)
TextButton17.MouseEnter:Connect(function(arg7)
	local tween26 = TweenService:Create(TextButton17, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(34, 34, 42) })
	tween26:Play()
end)
TextButton17.MouseLeave:Connect(function(arg8)
	local tween27 = TweenService:Create(TextButton17, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween27:Play()
end)
TextButton17.MouseButton1Click:Connect(function()
	local players5 = Players:GetPlayers()
	for i5, v5 in ipairs(players5) do
	end
	local HumanoidRootPart4 = Players.LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
	local HumanoidRootPart5 = v5.Character:FindFirstChild("HumanoidRootPart")
	HumanoidRootPart4.CFrame = (HumanoidRootPart5.CFrame + Vector3.new(0, 3, 0))
end)
local TextButton18 = Instance.new("TextButton")
TextButton18.LayoutOrder = 5
TextButton18.TextColor3 = Color3.fromRGB(235, 235, 240)
TextButton18.Parent = ScrollingFrame4
TextButton18.Text = "Teleport to Spawn"
TextButton18.AutoButtonColor = false
TextButton18.Font = Enum.Font.GothamBold
TextButton18.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
TextButton18.TextSize = 12
TextButton18.Size = UDim2.new(1, -8, 0, 30)
local UICorner48 = Instance.new("UICorner")
UICorner48.Parent = TextButton18
UICorner48.CornerRadius = UDim.new(0, 6)
TextButton18.MouseEnter:Connect(function(arg9)
	local tween28 = TweenService:Create(TextButton18, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(34, 34, 42) })
	tween28:Play()
end)
TextButton18.MouseLeave:Connect(function(arg10)
	local tween29 = TweenService:Create(TextButton18, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(26, 26, 32) })
	tween29:Play()
end)
TextButton18.MouseButton1Click:Connect(function()
	local HumanoidRootPart6 = Players.LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
	local SpawnLocation = workspace:FindFirstChildOfClass("SpawnLocation")
	HumanoidRootPart6.CFrame = (SpawnLocation.CFrame + Vector3.new(0, 5, 0))
end)
local ScrollingFrame6 = Instance.new("ScrollingFrame")
ScrollingFrame6.ScrollBarImageColor3 = Color3.fromRGB(90, 65, 165)
ScrollingFrame6.AutomaticCanvasSize = Enum.AutomaticSize.Y
ScrollingFrame6.ScrollBarThickness = 3
ScrollingFrame6.Parent = Frame6
ScrollingFrame6.Name = "Fun"
ScrollingFrame6.Visible = false
ScrollingFrame6.BackgroundTransparency = 1
ScrollingFrame6.CanvasSize = UDim2.new(0, 0, 0, 0)
ScrollingFrame6.BorderSizePixel = 0
ScrollingFrame6.Size = UDim2.fromScale(1, 1)
local UIListLayout7 = Instance.new("UIListLayout")
UIListLayout7.Parent = ScrollingFrame6
UIListLayout7.Padding = UDim.new(0, 8)
UIListLayout7.SortOrder = Enum.SortOrder.LayoutOrder
local UIPadding7 = Instance.new("UIPadding")
UIPadding7.PaddingTop = UDim.new(0, 6)
UIPadding7.PaddingBottom = UDim.new(0, 6)
UIPadding7.Parent = ScrollingFrame6
UIPadding7.PaddingRight = UDim.new(0, 6)
UIPadding7.PaddingLeft = UDim.new(0, 6)
local TextLabel28 = Instance.new("TextLabel")
TextLabel28.LayoutOrder = 1
TextLabel28.TextColor3 = Color3.fromRGB(150, 150, 165)
TextLabel28.Parent = ScrollingFrame6
TextLabel28.Text = "CHAOS"
TextLabel28.Font = Enum.Font.GothamBold
TextLabel28.BackgroundTransparency = 1
TextLabel28.TextXAlignment = Enum.TextXAlignment.Left
TextLabel28.TextSize = 10
TextLabel28.Size = UDim2.new(1, 0, 0, 18)
local Frame47 = Instance.new("Frame")
Frame47.LayoutOrder = 2
Frame47.Parent = ScrollingFrame6
Frame47.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame47.BorderSizePixel = 0
Frame47.Size = UDim2.new(1, -8, 0, 32)
local UICorner49 = Instance.new("UICorner")
UICorner49.Parent = Frame47
UICorner49.CornerRadius = UDim.new(0, 6)
local TextLabel29 = Instance.new("TextLabel")
TextLabel29.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel29.Parent = Frame47
TextLabel29.Text = "Rainbow Body"
TextLabel29.Font = Enum.Font.Gotham
TextLabel29.BackgroundTransparency = 1
TextLabel29.Position = UDim2.fromOffset(12, 0)
TextLabel29.TextXAlignment = Enum.TextXAlignment.Left
TextLabel29.TextSize = 12
TextLabel29.Size = UDim2.new(1, -60, 1, 0)
local Frame48 = Instance.new("Frame")
Frame48.Position = UDim2.new(1, -50, 0.5, -10)
Frame48.Parent = Frame47
Frame48.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame48.BorderSizePixel = 0
Frame48.Size = UDim2.fromOffset(40, 20)
local UICorner50 = Instance.new("UICorner")
UICorner50.Parent = Frame48
UICorner50.CornerRadius = UDim.new(0, 10)
local Frame49 = Instance.new("Frame")
Frame49.Position = UDim2.fromOffset(2, 2)
Frame49.Parent = Frame48
Frame49.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame49.BorderSizePixel = 0
Frame49.Size = UDim2.fromOffset(16, 16)
local UICorner51 = Instance.new("UICorner")
UICorner51.Parent = Frame49
UICorner51.CornerRadius = UDim.new(0, 8)
local TextButton19 = Instance.new("TextButton")
TextButton19.Parent = Frame47
TextButton19.Text = ""
TextButton19.BackgroundTransparency = 1
TextButton19.Size = UDim2.fromScale(1, 1)
TextButton19.MouseButton1Click:Connect(function()
	local tween30 = TweenService:Create(Frame48, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween30:Play()
	local tween31 = TweenService:Create(Frame49, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween31:Play()
end)
local Frame50 = Instance.new("Frame")
Frame50.LayoutOrder = 3
Frame50.Parent = ScrollingFrame6
Frame50.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
Frame50.BorderSizePixel = 0
Frame50.Size = UDim2.new(1, -8, 0, 32)
local UICorner52 = Instance.new("UICorner")
UICorner52.Parent = Frame50
UICorner52.CornerRadius = UDim.new(0, 6)
local TextLabel30 = Instance.new("TextLabel")
TextLabel30.TextColor3 = Color3.fromRGB(235, 235, 240)
TextLabel30.Parent = Frame50
TextLabel30.Text = "Spin"
TextLabel30.Font = Enum.Font.Gotham
TextLabel30.BackgroundTransparency = 1
TextLabel30.Position = UDim2.fromOffset(12, 0)
TextLabel30.TextXAlignment = Enum.TextXAlignment.Left
TextLabel30.TextSize = 12
TextLabel30.Size = UDim2.new(1, -60, 1, 0)
local Frame51 = Instance.new("Frame")
Frame51.Position = UDim2.new(1, -50, 0.5, -10)
Frame51.Parent = Frame50
Frame51.BackgroundColor3 = Color3.fromRGB(34, 34, 42)
Frame51.BorderSizePixel = 0
Frame51.Size = UDim2.fromOffset(40, 20)
local UICorner53 = Instance.new("UICorner")
UICorner53.Parent = Frame51
UICorner53.CornerRadius = UDim.new(0, 10)
local Frame52 = Instance.new("Frame")
Frame52.Position = UDim2.fromOffset(2, 2)
Frame52.Parent = Frame51
Frame52.BackgroundColor3 = Color3.fromRGB(150, 150, 165)
Frame52.BorderSizePixel = 0
Frame52.Size = UDim2.fromOffset(16, 16)
local UICorner54 = Instance.new("UICorner")
UICorner54.Parent = Frame52
UICorner54.CornerRadius = UDim.new(0, 8)
local TextButton20 = Instance.new("TextButton")
TextButton20.Parent = Frame50
TextButton20.Text = ""
TextButton20.BackgroundTransparency = 1
TextButton20.Size = UDim2.fromScale(1, 1)
TextButton20.MouseButton1Click:Connect(function()
	local tween32 = TweenService:Create(Frame51, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween32:Play()
	local tween33 = TweenService:Create(Frame52, TweenInfo.new(0.15), { BackgroundColor3 = Color3.new(1, 1, 1), Position = UDim2.fromOffset(22, 2) })
	tween33:Play()
end)
local TextButton21 = Instance.new("TextButton")
TextButton21.LayoutOrder = 4
TextButton21.TextColor3 = Color3.fromRGB(235, 235, 240)
TextButton21.Parent = ScrollingFrame6
TextButton21.Text = "Random Character Size"
TextButton21.AutoButtonColor = false
TextButton21.Font = Enum.Font.GothamBold
TextButton21.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
TextButton21.TextSize = 12
TextButton21.Size = UDim2.new(1, -8, 0, 30)
local UICorner55 = Instance.new("UICorner")
UICorner55.Parent = TextButton21
UICorner55.CornerRadius = UDim.new(0, 6)
TextButton21.MouseEnter:Connect(function(arg11)
	local tween34 = TweenService:Create(TextButton21, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(34, 34, 42) })
	tween34:Play()
end)
TextButton21.MouseLeave:Connect(function(arg12)
	local tween35 = TweenService:Create(TextButton21, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(26, 26, 32) })
	tween35:Play()
end)
TextButton21.MouseButton1Click:Connect(function()
	local Humanoid5 = Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
	local BodyHeightScale = Humanoid5:FindFirstChild("BodyHeightScale")
	BodyHeightScale.Value = 1.59
	local BodyWidthScale = Humanoid5:FindFirstChild("BodyWidthScale")
	BodyWidthScale.Value = 1.59
	local BodyDepthScale = Humanoid5:FindFirstChild("BodyDepthScale")
	BodyDepthScale.Value = 1.59
	local HeadScale = Humanoid5:FindFirstChild("HeadScale")
	HeadScale.Value = 1.59
end)
local TextButton22 = Instance.new("TextButton")
TextButton22.LayoutOrder = 5
TextButton22.TextColor3 = Color3.fromRGB(235, 235, 240)
TextButton22.Parent = ScrollingFrame6
TextButton22.Text = "Reset Size"
TextButton22.AutoButtonColor = false
TextButton22.Font = Enum.Font.GothamBold
TextButton22.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
TextButton22.TextSize = 12
TextButton22.Size = UDim2.new(1, -8, 0, 30)
local UICorner56 = Instance.new("UICorner")
UICorner56.Parent = TextButton22
UICorner56.CornerRadius = UDim.new(0, 6)
TextButton22.MouseEnter:Connect(function(arg13)
	local tween36 = TweenService:Create(TextButton22, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(34, 34, 42) })
	tween36:Play()
end)
TextButton22.MouseLeave:Connect(function(arg14)
	local tween37 = TweenService:Create(TextButton22, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(26, 26, 32) })
	tween37:Play()
end)
TextButton22.MouseButton1Click:Connect(function()
	local Humanoid6 = Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
	local BodyHeightScale2 = Humanoid6:FindFirstChild("BodyHeightScale")
	BodyHeightScale2.Value = 1
	local BodyWidthScale2 = Humanoid6:FindFirstChild("BodyWidthScale")
	BodyWidthScale2.Value = 1
	local BodyDepthScale2 = Humanoid6:FindFirstChild("BodyDepthScale")
	BodyDepthScale2.Value = 1
	local HeadScale2 = Humanoid6:FindFirstChild("HeadScale")
	HeadScale2.Value = 1
end)
local TextButton23 = Instance.new("TextButton")
TextButton23.LayoutOrder = 6
TextButton23.TextColor3 = Color3.fromRGB(235, 235, 240)
TextButton23.Parent = ScrollingFrame6
TextButton23.Text = "Seizure Mode (5s)"
TextButton23.AutoButtonColor = false
TextButton23.Font = Enum.Font.GothamBold
TextButton23.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
TextButton23.TextSize = 12
TextButton23.Size = UDim2.new(1, -8, 0, 30)
local UICorner57 = Instance.new("UICorner")
UICorner57.Parent = TextButton23
UICorner57.CornerRadius = UDim.new(0, 6)
TextButton23.MouseEnter:Connect(function(arg15)
	local tween38 = TweenService:Create(TextButton23, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(34, 34, 42) })
	tween38:Play()
end)
TextButton23.MouseLeave:Connect(function(arg16)
	local tween39 = TweenService:Create(TextButton23, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(140, 100, 255) })
	tween39:Play()
end)
TextButton23.MouseButton1Click:Connect(function()
	task.spawn(function(...)
		local descendants = Players.LocalPlayer.Character:GetDescendants()
		for i6, v6 in ipairs(descendants) do
			v6.Color = Color3.fromRGB(121, 185, 54)
		end
		task.wait(0.05)
		local descendants2 = Players.LocalPlayer.Character:GetDescendants()
		for i7, v7 in ipairs(descendants2) do
			v7.Color = Color3.fromRGB(232, 129, 185)
		end
		task.wait(0.05)
		local descendants3 = Players.LocalPlayer.Character:GetDescendants()
		for i8, v8 in ipairs(descendants3) do
			v8.Color = Color3.fromRGB(63, 234, 210)
		end
		task.wait(0.05)
		local descendants4 = Players.LocalPlayer.Character:GetDescendants()
		for i9, v9 in ipairs(descendants4) do
			v9.Color = Color3.fromRGB(90, 32, 146)
		end
		task.wait(0.05)
		local descendants5 = Players.LocalPlayer.Character:GetDescendants()
		for i10, v10 in ipairs(descendants5) do
			v10.Color = Color3.fromRGB(4, 176, 225)
		end
		task.wait(0.05)
		local descendants6 = Players.LocalPlayer.Character:GetDescendants()
		for i11, v11 in ipairs(descendants6) do
			v11.Color = Color3.fromRGB(156, 155, 93)
		end
		task.wait(0.05)
		local descendants7 = Players.LocalPlayer.Character:GetDescendants()
		for i12, v12 in ipairs(descendants7) do
			v12.Color = Color3.fromRGB(185, 143, 210)
		end
		task.wait(0.05)
		local descendants8 = Players.LocalPlayer.Character:GetDescendants()
		for i13, v13 in ipairs(descendants8) do
			v13.Color = Color3.fromRGB(29, 46, 115)
		end
		task.wait(0.05)
		local descendants9 = Players.LocalPlayer.Character:GetDescendants()
		for i14, v14 in ipairs(descendants9) do
			v14.Color = Color3.fromRGB(215, 55, 191)
		end
		task.wait(0.05)
	end)
end)
local TextButton24 = Instance.new("TextButton")
TextButton24.LayoutOrder = 7
TextButton24.TextColor3 = Color3.fromRGB(235, 235, 240)
TextButton24.Parent = ScrollingFrame6
TextButton24.Text = "Launch Into Sky"
TextButton24.AutoButtonColor = false
TextButton24.Font = Enum.Font.GothamBold
TextButton24.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
TextButton24.TextSize = 12
TextButton24.Size = UDim2.new(1, -8, 0, 30)
local UICorner58 = Instance.new("UICorner")
UICorner58.Parent = TextButton24
UICorner58.CornerRadius = UDim.new(0, 6)
TextButton24.MouseEnter:Connect(function(arg17)
	local tween40 = TweenService:Create(TextButton24, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(34, 34, 42) })
	tween40:Play()
end)
TextButton24.MouseLeave:Connect(function(arg18)
	local tween41 = TweenService:Create(TextButton24, TweenInfo.new(0.12), { BackgroundColor3 = Color3.fromRGB(26, 26, 32) })
	tween41:Play()
end)
TextButton24.MouseButton1Click:Connect(function()
	local HumanoidRootPart7 = Players.LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
	HumanoidRootPart7.Velocity = Vector3.new(0, 500, 0)
end)
local TextButton25 = Instance.new("TextButton")
TextButton25.LayoutOrder = 1
TextButton25.TextColor3 = Color3.fromRGB(150, 150, 165)
TextButton25.Parent = Frame5
TextButton25.Text = "Player"
TextButton25.AutoButtonColor = false
TextButton25.Font = Enum.Font.GothamBold
TextButton25.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
TextButton25.TextSize = 12
TextButton25.Size = UDim2.new(1, 0, 0, 30)
local UICorner59 = Instance.new("UICorner")
UICorner59.Parent = TextButton25
UICorner59.CornerRadius = UDim.new(0, 6)
local Frame53 = Instance.new("Frame")
Frame53.Visible = false
Frame53.Position = UDim2.new(0, 0, 0.2, 0)
Frame53.Parent = TextButton25
Frame53.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame53.BorderSizePixel = 0
Frame53.Size = UDim2.new(0, 3, 0.6, 0)
local UICorner60 = Instance.new("UICorner")
UICorner60.Parent = Frame53
UICorner60.CornerRadius = UDim.new(0, 2)
TextButton25.MouseButton1Click:Connect(function()
	ScrollingFrame.Visible = true
	Frame53.Visible = true
	local tween42 = TweenService:Create(TextButton25, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(34, 34, 42), TextColor3 = Color3.fromRGB(235, 235, 240) })
	tween42:Play()
	ScrollingFrame2.Visible = false
	Frame54.Visible = false
	local tween43 = TweenService:Create(TextButton26, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween43:Play()
	ScrollingFrame3.Visible = false
	Frame55.Visible = false
	local tween44 = TweenService:Create(TextButton27, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween44:Play()
	ScrollingFrame4.Visible = false
	Frame56.Visible = false
	local tween45 = TweenService:Create(TextButton28, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween45:Play()
	ScrollingFrame6.Visible = false
	Frame57.Visible = false
	local tween46 = TweenService:Create(TextButton29, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween46:Play()
end)
local TextButton26 = Instance.new("TextButton")
TextButton26.LayoutOrder = 2
TextButton26.TextColor3 = Color3.fromRGB(150, 150, 165)
TextButton26.Parent = Frame5
TextButton26.Text = "Visual"
TextButton26.AutoButtonColor = false
TextButton26.Font = Enum.Font.GothamBold
TextButton26.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
TextButton26.TextSize = 12
TextButton26.Size = UDim2.new(1, 0, 0, 30)
local UICorner61 = Instance.new("UICorner")
UICorner61.Parent = TextButton26
UICorner61.CornerRadius = UDim.new(0, 6)
local Frame54 = Instance.new("Frame")
Frame54.Visible = false
Frame54.Position = UDim2.new(0, 0, 0.2, 0)
Frame54.Parent = TextButton26
Frame54.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame54.BorderSizePixel = 0
Frame54.Size = UDim2.new(0, 3, 0.6, 0)
local UICorner62 = Instance.new("UICorner")
UICorner62.Parent = Frame54
UICorner62.CornerRadius = UDim.new(0, 2)
TextButton26.MouseButton1Click:Connect(function()
	ScrollingFrame.Visible = false
	Frame53.Visible = false
	local tween47 = TweenService:Create(TextButton25, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween47:Play()
	ScrollingFrame2.Visible = true
	Frame54.Visible = true
	local tween48 = TweenService:Create(TextButton26, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(34, 34, 42), TextColor3 = Color3.fromRGB(235, 235, 240) })
	tween48:Play()
	ScrollingFrame3.Visible = false
	Frame55.Visible = false
	local tween49 = TweenService:Create(TextButton27, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween49:Play()
	ScrollingFrame4.Visible = false
	Frame56.Visible = false
	local tween50 = TweenService:Create(TextButton28, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween50:Play()
	ScrollingFrame6.Visible = false
	Frame57.Visible = false
	local tween51 = TweenService:Create(TextButton29, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween51:Play()
end)
local TextButton27 = Instance.new("TextButton")
TextButton27.LayoutOrder = 3
TextButton27.TextColor3 = Color3.fromRGB(150, 150, 165)
TextButton27.Parent = Frame5
TextButton27.Text = "Movement"
TextButton27.AutoButtonColor = false
TextButton27.Font = Enum.Font.GothamBold
TextButton27.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
TextButton27.TextSize = 12
TextButton27.Size = UDim2.new(1, 0, 0, 30)
local UICorner63 = Instance.new("UICorner")
UICorner63.Parent = TextButton27
UICorner63.CornerRadius = UDim.new(0, 6)
local Frame55 = Instance.new("Frame")
Frame55.Visible = false
Frame55.Position = UDim2.new(0, 0, 0.2, 0)
Frame55.Parent = TextButton27
Frame55.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame55.BorderSizePixel = 0
Frame55.Size = UDim2.new(0, 3, 0.6, 0)
local UICorner64 = Instance.new("UICorner")
UICorner64.Parent = Frame55
UICorner64.CornerRadius = UDim.new(0, 2)
TextButton27.MouseButton1Click:Connect(function()
	ScrollingFrame.Visible = false
	Frame53.Visible = false
	local tween52 = TweenService:Create(TextButton25, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween52:Play()
	ScrollingFrame2.Visible = false
	Frame54.Visible = false
	local tween53 = TweenService:Create(TextButton26, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween53:Play()
	ScrollingFrame3.Visible = true
	Frame55.Visible = true
	local tween54 = TweenService:Create(TextButton27, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(34, 34, 42), TextColor3 = Color3.fromRGB(235, 235, 240) })
	tween54:Play()
	ScrollingFrame4.Visible = false
	Frame56.Visible = false
	local tween55 = TweenService:Create(TextButton28, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween55:Play()
	ScrollingFrame6.Visible = false
	Frame57.Visible = false
	local tween56 = TweenService:Create(TextButton29, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween56:Play()
end)
local TextButton28 = Instance.new("TextButton")
TextButton28.LayoutOrder = 4
TextButton28.TextColor3 = Color3.fromRGB(150, 150, 165)
TextButton28.Parent = Frame5
TextButton28.Text = "Teleport"
TextButton28.AutoButtonColor = false
TextButton28.Font = Enum.Font.GothamBold
TextButton28.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
TextButton28.TextSize = 12
TextButton28.Size = UDim2.new(1, 0, 0, 30)
local UICorner65 = Instance.new("UICorner")
UICorner65.Parent = TextButton28
UICorner65.CornerRadius = UDim.new(0, 6)
local Frame56 = Instance.new("Frame")
Frame56.Visible = false
Frame56.Position = UDim2.new(0, 0, 0.2, 0)
Frame56.Parent = TextButton28
Frame56.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame56.BorderSizePixel = 0
Frame56.Size = UDim2.new(0, 3, 0.6, 0)
local UICorner66 = Instance.new("UICorner")
UICorner66.Parent = Frame56
UICorner66.CornerRadius = UDim.new(0, 2)
TextButton28.MouseButton1Click:Connect(function()
	ScrollingFrame.Visible = false
	Frame53.Visible = false
	local tween57 = TweenService:Create(TextButton25, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween57:Play()
	ScrollingFrame2.Visible = false
	Frame54.Visible = false
	local tween58 = TweenService:Create(TextButton26, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween58:Play()
	ScrollingFrame3.Visible = false
	Frame55.Visible = false
	local tween59 = TweenService:Create(TextButton27, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween59:Play()
	ScrollingFrame4.Visible = true
	Frame56.Visible = true
	local tween60 = TweenService:Create(TextButton28, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(34, 34, 42), TextColor3 = Color3.fromRGB(235, 235, 240) })
	tween60:Play()
	ScrollingFrame6.Visible = false
	Frame57.Visible = false
	local tween61 = TweenService:Create(TextButton29, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween61:Play()
end)
local TextButton29 = Instance.new("TextButton")
TextButton29.LayoutOrder = 5
TextButton29.TextColor3 = Color3.fromRGB(150, 150, 165)
TextButton29.Parent = Frame5
TextButton29.Text = "Fun"
TextButton29.AutoButtonColor = false
TextButton29.Font = Enum.Font.GothamBold
TextButton29.BackgroundColor3 = Color3.fromRGB(26, 26, 32)
TextButton29.TextSize = 12
TextButton29.Size = UDim2.new(1, 0, 0, 30)
local UICorner67 = Instance.new("UICorner")
UICorner67.Parent = TextButton29
UICorner67.CornerRadius = UDim.new(0, 6)
local Frame57 = Instance.new("Frame")
Frame57.Visible = false
Frame57.Position = UDim2.new(0, 0, 0.2, 0)
Frame57.Parent = TextButton29
Frame57.BackgroundColor3 = Color3.fromRGB(140, 100, 255)
Frame57.BorderSizePixel = 0
Frame57.Size = UDim2.new(0, 3, 0.6, 0)
local UICorner68 = Instance.new("UICorner")
UICorner68.Parent = Frame57
UICorner68.CornerRadius = UDim.new(0, 2)
TextButton29.MouseButton1Click:Connect(function()
	ScrollingFrame.Visible = false
	Frame53.Visible = false
	local tween62 = TweenService:Create(TextButton25, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween62:Play()
	ScrollingFrame2.Visible = false
	Frame54.Visible = false
	local tween63 = TweenService:Create(TextButton26, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween63:Play()
	ScrollingFrame3.Visible = false
	Frame55.Visible = false
	local tween64 = TweenService:Create(TextButton27, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween64:Play()
	ScrollingFrame4.Visible = false
	Frame56.Visible = false
	local tween65 = TweenService:Create(TextButton28, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
	tween65:Play()
	ScrollingFrame6.Visible = true
	Frame57.Visible = true
	local tween66 = TweenService:Create(TextButton29, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(34, 34, 42), TextColor3 = Color3.fromRGB(235, 235, 240) })
	tween66:Play()
end)
ScrollingFrame.Visible = true
Frame53.Visible = true
local tween = TweenService:Create(TextButton25, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(34, 34, 42), TextColor3 = Color3.fromRGB(235, 235, 240) })
tween:Play()
ScrollingFrame2.Visible = false
Frame54.Visible = false
local tween2 = TweenService:Create(TextButton26, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
tween2:Play()
ScrollingFrame3.Visible = false
Frame55.Visible = false
local tween3 = TweenService:Create(TextButton27, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
tween3:Play()
ScrollingFrame4.Visible = false
Frame56.Visible = false
local tween4 = TweenService:Create(TextButton28, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
tween4:Play()
ScrollingFrame6.Visible = false
Frame57.Visible = false
local tween5 = TweenService:Create(TextButton29, TweenInfo.new(0.15), { BackgroundColor3 = Color3.fromRGB(26, 26, 32), TextColor3 = Color3.fromRGB(150, 150, 165) })
tween5:Play()
local Humanoid = Players.LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
Humanoid.WalkSpeed = 16
Humanoid.JumpPower = 50
Humanoid.UseJumpPower = true
workspace.CurrentCamera.FieldOfView = 70
workspace.Gravity = 196.2
StarterGui:SetCore("SendNotification", { Text = "Loaded. Drag the title bar. Have fun.", Title = "Random Things Hub", Duration = 4 })
