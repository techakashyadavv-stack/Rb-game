local part = script.Parent

part.Touched:Connect(function(hit)
	if game.Players:FindFirstChild(hit.Parent.Name) then
		local player = game.Players:FindFirstChild(hit.Parent.Name)
		player.leaderstats.Level.Value = part.Level.Value
	end
end)

