package com.example;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.config.SaslConfigs;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;

import java.util.Properties;

public class AccidentDetectionApp {
    private static String APPLICATION_NAME = "accident_detection_streams";
    private static String BOOTSTRAP_SERVERS = "b-1.common-dev-main.z52ehr.c2.kafka.ap-northeast-2.amazonaws.com:9096,b-2.common-dev-main.z52ehr.c2.kafka.ap-northeast-2.amazonaws.com:9096";
    private static String SASL_MECHANISM = "SCRAM-SHA-512";
    private static String INPUT_STREAM_LOG = "fii_vg";
    private static String OUTPUT_STREAM_FILTERED_LOG = "fii-accident-detected-info";
    private static String SECURITY_PROTOCOL = "SASL_SSL";
    private static Double ACC_THRESHOLD = Math.pow(25.0, 2);

    // TODO: 단계별 해결해야 되는 task (1, 2) 작업 해야됨
    // 1. MSK에 연결이 되는지 확인힌디. -> 연결하는 함수 생성
    // 2. topic 에서 record를 가져와야 한다. -> record 가져오는 함수 생성
    //    2-1. Serialized, Deserialized 방법을 정해줘야 되는데, 이게 compression type(gzip)과 관계가 있나? 아님 정해진 방법이 있나?

    // 3. record에서 key 값에 해당하는 value를 뽑아와야 한다. -> ax, ay 제곱합 하는 함수 생성
    // 4. 만들어진 value를 새로운 topic 에 쏴야한다.
    public static double calculate_xyacc(String s) {
        String[] pairs = s.split(",");
        double output = 0.0;
        for (int i=0; i<pairs.length; i++) {
            String pair = pairs[i];
            String[] keyValue = pair.split(":");

            if (keyValue[0].equals("mLocalAccelx") || keyValue[0].equals("mLocalAccely")) {
                double value = Integer.valueOf(keyValue[1]);
                output += Math.pow(value, 2);
            }
        }
        return output;
    }

    public static void main(String[] args) {

        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, APPLICATION_NAME);
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(SaslConfigs.SASL_MECHANISM, SASL_MECHANISM);
        props.put(StreamsConfig.SECURITY_PROTOCOL_CONFIG, SECURITY_PROTOCOL);
//        https://kafka.apache.org/25/javadoc/constant-values.html 참고함.
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        StreamsBuilder builder = new StreamsBuilder();
        KStream<String, String> streamLog = builder.stream(INPUT_STREAM_LOG);
        KStream<String, String> filteredStream = streamLog.filter(
                (key, value) -> calculate_xyacc(value) >= ACC_THRESHOLD);
        filteredStream.to(OUTPUT_STREAM_FILTERED_LOG);

        KafkaStreams streams;
        streams = new KafkaStreams(builder.build(), props);
        streams.start();
    }
}
