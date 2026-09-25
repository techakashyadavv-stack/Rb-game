local TweenServices = game:GetService("TweenService")
local part = script.Parent
local tweenInfo = TweenInfo.new(1, Enum.EasingStyle.Linear, Enum.EasingDirection.InOut, -1, true)
local tween = TweenServices:Create(part, tweenInfo, {Position = part.Position + Vector3.new(0, 15, 0)})
tween:Play()