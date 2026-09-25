
game.Players.PlayerAdded:Connect(function(plr)
	local leaderstats = Instance.new("Folder", plr)
	leaderstats.Name = "leaderstats"
	local level = Instance.new("IntValue", leaderstats)
	level.Name = "Level"
	level.Value = 0
end)