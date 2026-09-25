local mps = game:GetService("MarketplaceService")

local id = 3714741432

-- Robux purchases must be granted here; Roblox retries (and eventually refunds)
-- any receipt that is not answered with PurchaseGranted.
mps.ProcessReceipt = function(receipt)
	if receipt.ProductId ~= id then
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	local plr = game.Players:GetPlayerByUserId(receipt.PlayerId)
	if not plr then
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	local level = plr.leaderstats.Level
	for i, checkpoint in pairs(workspace.Checkpoints:GetChildren()) do
		if checkpoint.Level.Value == level.Value + 1 then
			level.Value += 1
			if plr.Character then
				plr.Character:PivotTo(CFrame.new(checkpoint.Position + Vector3.new(0,5,0)))
			end

			return Enum.ProductPurchaseDecision.PurchaseGranted
		end
	end

	-- Already at the last checkpoint: nothing to skip to, so don't take the Robux.
	return Enum.ProductPurchaseDecision.NotProcessedYet
end
