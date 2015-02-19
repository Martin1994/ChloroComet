var ChloroCometClient = function (url, token)
{
    /* Properties */

    this.token = token;
    this.method = undefined;
    this.url = url;
    this.secure = window.location.href.substr(0, 8) == "https://";

    if (typeof ChloroCometClient._initialized == "undefined") {

        /* Methods */

        ChloroCometClient.prototype.connect = function () {
            if (this.method == "WebSocket") {
                this.connectWS();
            } else {
                this.connectStream();
            }
        };

        ChloroCometClient.prototype.connectWS = function () {
            var ws = new WebSocket((this.secure ? "wss://" : "ws://") + this.url + "/api/websocket?token=" + this.token);

            ws.onmessage = (function (client) {
                return function (event) {
                    client.onMessage({
                        message: event.data
                    });
                }
            })(this);

            ws.onclose = (function (client) {
                return function (event) {
                    if (event.code != 1006) {
                        client.connect();
                    }
                }
            })(this);
        };

        ChloroCometClient.prototype.connectStream = function () {
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.lastResponseLength = 0;

            xmlhttp.onreadystatechange = (function (client, xmlhttp) {
                return function (event) {
                    if (xmlhttp.readyState == 3) {
                        client.onMessage({
                            message: xmlhttp.responseText.substr(xmlhttp.lastResponseLength)
                        });
                        xmlhttp.lastResponseLength = xmlhttp.responseText.length;
                    } else if (xmlhttp.readyState == 4) {
                        client.connect;
                    }
                }
            })(this, xmlhttp);

            xmlhttp.open("GET", (this.secure ? "https://" : "http://") + this.url + "/api/comet?token=" + this.token);
            xmlhttp.send();
        };

        // event = { message: "received message" }
        ChloroCometClient.prototype.onMessage = function (event) {
            throw "ChloroComet: onMessage is not binded."
        };

        ChloroCometClient.prototype._constructor = function () {
            if (this.url.charAt(this.url.length - 1) == "/") {
                this.url = this.url.substr(0, this.url.length - 1);
            }
            if (typeof window.WebSocket == "undefined") {
                this.method = "Streaming";
            } else {
                this.method = "WebSocket";
            }
            this.connect();
        };

        ChloroCometClient._initialized = true;
    }

    this._constructor();
};