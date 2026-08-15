/*
  Example YARA rules - EDUCATIONAL, pattern-based indicators only.
  These look for generic strings/behaviors often seen in ransom notes
  and ransomware binaries. They do NOT contain any malicious code.
*/

rule Suspicious_Ransom_Note_Text
{
    meta:
        description = "Detects common ransom note wording in a text file"
        mitre = "T1486"
    strings:
        $s1 = "your files have been encrypted" nocase
        $s2 = "decrypt your files" nocase
        $s3 = "bitcoin" nocase
        $s4 = "pay the ransom" nocase
        $s5 = "private key" nocase
    condition:
        2 of ($s1, $s2, $s3, $s4, $s5)
}

rule Suspicious_Shadow_Copy_Deletion_String
{
    meta:
        description = "Binary references vssadmin/wmic shadow copy deletion (common anti-recovery step)"
        mitre = "T1490"
    strings:
        $s1 = "vssadmin delete shadows" nocase
        $s2 = "wmic shadowcopy delete" nocase
        $s3 = "bcdedit /set" nocase
    condition:
        any of them
}
