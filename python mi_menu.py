local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local player = Players.LocalPlayer
local camera = workspace.CurrentCamera

-- Variables de control
local aimAssistActive = false
local aimbotActive = false
local aimRange = 150
local smoothness = 0.2

-- Crear GUI
local screenGui = Instance.new("ScreenGui")
screenGui.Parent = player:WaitForChild("PlayerGui")

local frame = Instance.new("Frame")
frame.Size = UDim2.new(0, 250, 0, 200)
frame.Position = UDim2.new(1, -270, 1, -220)
frame.BackgroundColor3 = Color3.fromRGB(20, 20, 20)
frame.BorderSizePixel = 0
frame.BackgroundTransparency = 0.1
frame.Parent = screenGui

local shadow = Instance.new("Frame")
shadow.Size = UDim2.new(1, 10, 1, 10)
shadow.Position = UDim2.new(0, -5, 0, -5)
shadow.BackgroundColor3 = Color3.fromRGB(10, 10, 10)
shadow.BackgroundTransparency = 0.5
shadow.ZIndex = -1
shadow.Parent = frame

local title = Instance.new("TextLabel")
title.Size = UDim2.new(1, 0, 0, 40)
title.Text = "By: monitonac"
title.TextColor3 = Color3.fromRGB(255, 255, 255)
title.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
title.Font = Enum.Font.GothamBold
title.TextSize = 24
title.Parent = frame

local closeButton = Instance.new("TextButton")
closeButton.Size = UDim2.new(0, 30, 0, 30)
closeButton.Position = UDim2.new(1, -35, 0, 5)
closeButton.Text = "X"
closeButton.TextColor3 = Color3.fromRGB(255, 100, 100)
closeButton.BackgroundColor3 = Color3.fromRGB(40, 40, 40)
closeButton.Font = Enum.Font.GothamBold
closeButton.Parent = frame

local aimAssistButton = Instance.new("TextButton")
aimAssistButton.Size = UDim2.new(1, 0, 0, 50)
aimAssistButton.Position = UDim2.new(0, 0, 0, 50)
aimAssistButton.Text = "Aim Assist: OFF"
aimAssistButton.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
aimAssistButton.TextColor3 = Color3.fromRGB(255, 255, 255)
aimAssistButton.Font = Enum.Font.Gotham
aimAssistButton.Parent = frame

local aimbotButton = Instance.new("TextButton")
aimbotButton.Size = UDim2.new(1, 0, 0, 50)
aimbotButton.Position = UDim2.new(0, 0, 0, 110)
aimbotButton.Text = "Aimbot: OFF"
aimbotButton.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
aimbotButton.TextColor3 = Color3.fromRGB(255, 255, 255)
aimbotButton.Font = Enum.Font.Gotham
aimbotButton.Parent = frame

-- Función para obtener el objetivo más cercano
local function getClosestTarget()
    local closestTarget = nil
    local shortestDistance = aimRange

    for _, otherPlayer in ipairs(Players:GetPlayers()) do
        if otherPlayer ~= player and otherPlayer.Character and otherPlayer.Character:FindFirstChild("HumanoidRootPart") then
            local targetPosition = otherPlayer.Character.HumanoidRootPart.Position
            local screenPoint, onScreen = camera:WorldToViewportPoint(targetPosition)
            local mousePos = UserInputService:GetMouseLocation()
            local distance = (Vector2.new(screenPoint.X, screenPoint.Y) - mousePos).magnitude

            if onScreen and distance < shortestDistance then
                shortestDistance = distance
                closestTarget = otherPlayer.Character.HumanoidRootPart
            end
        end
    end

    return closestTarget
end

-- Función de Aim Assist (suave)
local function aimAssist()
    local target = getClosestTarget()
    if target then
        local direction = (target.Position - camera.CFrame.Position).unit
        local newCFrame = CFrame.new(camera.CFrame.Position, camera.CFrame.Position + direction)
        camera.CFrame = camera.CFrame:Lerp(newCFrame, smoothness)
    end
end

-- Función de Aimbot (instantáneo)
local function aimbot()
    local target = getClosestTarget()
    if target then
        local direction = (target.Position - camera.CFrame.Position).unit
        camera.CFrame = CFrame.new(camera.CFrame.Position, camera.CFrame.Position + direction)
    end
end

-- Eventos de los botones
aimAssistButton.MouseButton1Click:Connect(function()
    aimAssistActive = not aimAssistActive
    aimAssistButton.Text = aimAssistActive and "Aim Assist: ON" or "Aim Assist: OFF"
end)

aimbotButton.MouseButton1Click:Connect(function()
    aimbotActive = not aimbotActive
    aimbotButton.Text = aimbotActive and "Aimbot: ON" or "Aimbot: OFF"
end)

closeButton.MouseButton1Click:Connect(function()
    screenGui:Destroy()
end)

-- Actualización constante
RunService.RenderStepped:Connect(function()
    if aimAssistActive then
        aimAssist()
    end
    if aimbotActive then
        aimbot()
    end
end)