scriptName := "Retail"    ; ← Change this to "Retail", "InventorySync", etc.
guid := GetPC_GUID()
timestamp := A_Now

url := "https://web-production-31dc.up.railway.app/get_script?script=" . scriptName . "&guid=" . guid . "&t=" . timestamp

Http := ComObjCreate("WinHttp.WinHttpRequest.5.1")
Http.Open("GET", url, false)
Http.Send()
code := Http.ResponseText

file := A_Temp "\temp_ahk_run.ahk"
FileDelete, %file%
FileAppend, %code%, %file%
Run, %A_AhkPath% "%file%"
ExitApp

GetPC_GUID() {
    obj := ComObjGet("winmgmts:\\.\root\cimv2")
    for itm in obj.ExecQuery("Select * from Win32_ComputerSystemProduct")
        return StrReplace(itm.UUID, "-")
}
