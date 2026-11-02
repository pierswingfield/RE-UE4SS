function Register()
    return "48 8B 0D ? ? ? ? 48 85 C9 74 0A 48 8B 01 48 8B 40 28 48 FF E0"
end

function OnMatchFound(MatchAddress)
    return MatchAddress + 7 + DerefToInt32(MatchAddress + 3)
end
