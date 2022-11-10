import io.github.cdimascio.dotenv.dotenv
import algorithms.lv0.ADalgorithmLv0
import org.apache.kafka.common.config.SaslConfigs
import org.apache.kafka.common.serialization.Serdes
import org.apache.kafka.streams.KafkaStreams
import org.apache.kafka.streams.StreamsBuilder
import org.apache.kafka.streams.StreamsConfig
import java.util.*

object EmptyTopicRecords {
    val APPLICATION_NAME = "accident_detection_streams"
    val BOOTSTRAP_SERVERS = dotenv()["BOOTSTRAP_SERVERS"]
    val SASL_MECHANISM = dotenv()["SASL_MECHANISM"]
    val INPUT_STREAM_LOG = dotenv()["TOPIC_FII_SIMULATOR_RF2"]
    val OUTPUT_STREAM_FILTERED_LOG = dotenv()["TOPIC_FII_ACCIDENT_DETECTED_INFO"]
    val SECURITY_PROTOCOL = dotenv()["SECURITY_PROTOCOL"]
    val ACC_THRESHOLD = dotenv()["AD_ALGORITHM_THRESHOLD"].toDouble()

    @JvmStatic
    fun main(args: Array<String>) {
        val props = Properties()
        props[StreamsConfig.APPLICATION_ID_CONFIG] = APPLICATION_NAME
        props[StreamsConfig.BOOTSTRAP_SERVERS_CONFIG] = BOOTSTRAP_SERVERS
        props[SaslConfigs.SASL_MECHANISM] = SASL_MECHANISM
        props[StreamsConfig.SECURITY_PROTOCOL_CONFIG] = SECURITY_PROTOCOL
        System.setProperty("java.security.auth.login.config", "jass.conf")

        props[StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG] = Serdes.String().javaClass
        props[StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG] = Serdes.String().javaClass
        val builder = StreamsBuilder()
        val streamLog = builder.stream<String, String>(INPUT_STREAM_LOG)

        streamLog.to(OUTPUT_STREAM_FILTERED_LOG)

        val streams: KafkaStreams = KafkaStreams(builder.build(), props)
        streams.start()
    }
}
