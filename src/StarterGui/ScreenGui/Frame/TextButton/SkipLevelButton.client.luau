local mps = game:GetService("MarketplaceService")
local devKey = 3714741432
script.Parent.MouseButton1Up:Connect(function()
	mps:PromptProductPurchase(game.Players.LocalPlayer, devKey)
end)