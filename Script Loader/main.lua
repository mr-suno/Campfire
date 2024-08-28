--[[

    SETITNGS:

    -- toLoad:
    -     "a": Starry BETA
    -     "b": Infinite Yield Admin
    -     "c": Dex Explorer

]]

local toLoad = _G.toLoad
toLoad = toLoad:lower()

if toLoad == "b" then
    loadstring(game:HttpGet('https://raw.githubusercontent.com/EdgeIY/infiniteyield/master/source'))()
elseif toLoad == "a" then
    loadstring(game:HttpGet("https://github.com/mr-suno/Starry/blob/main/version/preview.lua?raw=true"))()
elseif toLoad == "c" then
    loadstring(game:HttpGet("https://raw.githubusercontent.com/infyiff/backup/main/dex.lua"))()
end
