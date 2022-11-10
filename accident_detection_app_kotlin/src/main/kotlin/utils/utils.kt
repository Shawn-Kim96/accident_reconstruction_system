package utils


fun SplitStringByCharacter (s: String, char: String) : Array<String> {
    return s.split(char.toRegex()).dropLastWhile { it.isEmpty() }.toTypedArray()
}
