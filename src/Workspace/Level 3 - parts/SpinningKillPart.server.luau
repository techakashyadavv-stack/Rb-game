local part = script.Parent
local TweenServices = game:GetService("TweenService")
local tweenInfo = TweenInfo.new(2, Enum.EasingStyle.Linear, Enum.EasingDirection.InOut, -1, false)
local tween = TweenServices:Create(part, tweenInfo, {Orientation = Vector3.new(0, 360, 0)})
tween:Play()

part.Touched:Connect(function(hit)
	local humanoid = hit.Parent:FindFirstChildOfClass("Humanoid")
	if humanoid then
		humanoid.Health = 0
	end
end)