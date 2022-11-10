package algorithms.lv0

import kotlin.math.pow
import utils.*

fun ADalgorithmLv0(s: String?): Double {
    val pairs = when {
        s.isNullOrBlank() -> arrayOf("blank:data")
        else -> SplitStringByCharacter(s, ",")
    }
    var output = 0.0
    for (pair in pairs) {
        val keyValue = SplitStringByCharacter(pair, ":")
        val AccColumn: Array<String> = arrayOf("mLocalAccelx", "mLocalAccely", "mLocalAccelz")
        if (AccColumn.contains(keyValue[0])) {
            val sensorData = when {
                keyValue[1] == "NaN" -> 0.0
                keyValue[1].toDoubleOrNull() == null -> keyValue[1].split("}").toTypedArray()[0].toDouble()
                else -> keyValue[1].toDouble()
            }
            output += sensorData.pow(2.0)
        }
    }
    return output
}
