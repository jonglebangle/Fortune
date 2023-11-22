import sys
import selectors
import json
import io
import struct

request_search = {
    "금전운": [
        "재테크를 시작하는 좋은 날입니다.",
        "돈이 예상보다 많이 들어올 것 같아요.",
        "신중한 투자가 필요한 시기입니다.",
        "재물운이 밝아지고 있어요.",
        "금전적인 기회가 찾아올 것입니다.",
        "안전한 투자가 금전을 지킬 수 있어요.",
        "새로운 수입의 문이 열릴 것입니다.",
        "금전적으로 안정된 상태를 유지하세요.",
        "재물운이 증가하고 있어 행복한 시기입니다.",
        "돈을 모으는 노력이 빛을 발할 것입니다.",
        "돈이 예상보다 많이 나가는 날입니다.",
        "금전적인 문제에 대비하는 것이 좋아보입니다.",
    ],
    "사업운": [
        "사업이 크게 번창할 것입니다.",
        "새로운 사업 기회가 찾아올 것입니다.",
        "사업 파트너십이 중요한 시기입니다.",
        "전략을 세워 사업을 확장하세요.",
        "사업의 안정적인 성장이 기대됩니다.",
        "새로운 시장 진출이 성공할 것입니다.",
        "사업 전문가의 조언을 듣는 것이 도움이 될 것입니다.",
        "사업 파트너와의 협력이 성공적일 것입니다.",
        "고객과의 소통을 강화하세요.",
        "사업의 비전과 목표를 명확히하세요.",
        "사업이 어려움에 부딪힐 것입니다.",
        "경제 환경 변화에 대비하는 것이 필요해보입니다.",
    ],
    "건강운": [
        "건강한 식습관을 유지하세요.",
        "규칙적인 운동이 건강에 도움이 됩니다.",
        "스트레스 관리에 신경 써야 합니다.",
        "매일 충분한 수면을 취하세요.",
        "신선한 과일과 채소를 많이 섭취하세요.",
        "걷기나 조깅과 같은 유산소 운동이 좋습니다.",
        "정기적인 건강 검진을 받으세요.",
        "스트레칭이 몸의 유연성을 향상시킵니다.",
        "햇볕에 자주 노출되어 비타민 D를 얻으세요.",
        "건강한 라이프스타일을 즐기세요.",
        "건강에 부정적인 영향을 미칠 요소에 주의하세요.",
        "건강 문제에 대비하는 것이 필요해보입니다.",
    ],
    "연애운": [
        "새로운 인연이 시작될 것입니다.",
        "상대방과 소통이 원활해질 것입니다.",
        "감정 표현을 솔직하게 해보세요.",
        "좋은 인연을 유지하기 위해 노력해야 합니다.",
        "소소한 데이트가 행복을 가져올 것입니다.",
        "서로의 관심사를 공유하세요.",
        "존중과 신뢰를 기반으로 관계를 성장시켜보세요.",
        "서로에게 공간을 주고 존중하는 것이 중요합니다.",
        "긍정적인 마음으로 상대방을 바라봐보세요.",
        "서로에게 응원과 격려를 주는 관계가 중요합니다.",
        "연인 간의 의사소통이 중요한 시기입니다.",
        "연애 생활에 변화가 예상되는 날입니다.",
    ],
    "랜덤": [
        "재테크를 시작하는 좋은 날입니다.",
        "돈이 예상보다 많이 들어올 것 같아요.",
        "신중한 투자가 필요한 시기입니다.",
        "재물운이 밝아지고 있어요.",
        "금전적인 기회가 찾아올 것입니다.",
        "안전한 투자가 금전을 지킬 수 있어요.",
        "새로운 수입의 문이 열릴 것입니다.",
        "금전적으로 안정된 상태를 유지하세요.",
        "재물운이 증가하고 있어 행복한 시기입니다.",
        "돈을 모으는 노력이 빛을 발할 것입니다.",
        "돈이 예상보다 많이 나가는 날입니다.",
        "금전적인 문제에 대비하는 것이 좋아보입니다.",
        "사업이 크게 번창할 것입니다.",
        "새로운 사업 기회가 찾아올 것입니다.",
        "사업 파트너십이 중요한 시기입니다.",
        "전략을 세워 사업을 확장하세요.",
        "사업의 안정적인 성장이 기대됩니다.",
        "새로운 시장 진출이 성공할 것입니다.",
        "사업 전문가의 조언을 듣는 것이 도움이 될 것입니다.",
        "사업 파트너와의 협력이 성공적일 것입니다.",
        "고객과의 소통을 강화하세요.",
        "사업의 비전과 목표를 명확히하세요.",
        "사업이 어려움에 부딪힐 것입니다.",
        "경제 환경 변화에 대비하는 것이 필요해보입니다.",
        "건강한 식습관을 유지하세요.",
        "규칙적인 운동이 건강에 도움이 됩니다.",
        "스트레스 관리에 신경 써야 합니다.",
        "매일 충분한 수면을 취하세요.",
        "신선한 과일과 채소를 많이 섭취하세요.",
        "걷기나 조깅과 같은 유산소 운동이 좋습니다.",
        "정기적인 건강 검진을 받으세요.",
        "스트레칭이 몸의 유연성을 향상시킵니다.",
        "햇볕에 자주 노출되어 비타민 D를 얻으세요.",
        "건강한 라이프스타일을 즐기세요.",
        "건강에 부정적인 영향을 미칠 요소에 주의하세요.",
        "건강 문제에 대비하는 것이 필요해보입니다.",
        "새로운 인연이 시작될 것입니다.",
        "상대방과 소통이 원활해질 것입니다.",
        "감정 표현을 솔직하게 해보세요.",
        "좋은 인연을 유지하기 위해 노력해야 합니다.",
        "소소한 데이트가 행복을 가져올 것입니다.",
        "서로의 관심사를 공유하세요.",
        "존중과 신뢰를 기반으로 관계를 성장시켜보세요.",
        "서로에게 공간을 주고 존중하는 것이 중요합니다.",
        "긍정적인 마음으로 상대방을 바라봐보세요.",
        "서로에게 응원과 격려를 주는 관계가 중요합니다.",
        "연인 간의 의사소통이 중요한 시기입니다.",
        "연애 생활에 변화가 예상되는 날입니다.",
    ],
    "종료": [
        "이용해주셔서 감사합니다!",
    ],
}



class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {mode!r}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    self.close()

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _create_response_json_content(self):
        action = self.request.get("action")
        if action == "search":
            query = self.request.get("value")
            answer = request_search.get(query) or f"No match for '{query}'."
            content = {"result": answer}
        else:
            content = {"result": f"Error: invalid action '{action}'."}
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

    def _create_response_binary_content(self):
        response = {
            "content_bytes": b"First 10 bytes of request: "
            + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

    def close(self):
        print(f"Closing connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"Error: selector.unregister() exception for "
                f"{self.addr}: {e!r}"
            )

        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")

    def process_request(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            print(f"Received request {self.request!r} from {self.addr}")
        else:
            # Binary or unknown content-type
            self.request = data
            print(
                f"Received {self.jsonheader['content-type']} "
                f"request from {self.addr}"
            )
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message
