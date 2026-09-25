game.Players.PlayerAdded:Connect(function(plr)
	plr.CharacterAdded:Connect(function(char)
		local level = plr:WaitForChild("leaderstats"):WaitForChild("Level").Value
		for i, checkpoint in pairs(workspace:WaitForChild("Checkpoints"):GetChildren()) do
			if checkpoint.Level.Value == level then
				task.wait(.5)
				char:PivotTo(CFrame.new(checkpoint.Position + Vector3.new(0,5,0)))
			end
		end
	end)
end)