use wasm_bindgen::prelude::*;
use wasm_bindgen::JsCast;
use web_sys::{
    MessageEvent, RtcDataChannel, RtcPeerConnection, WebSocket,
    RtcConfiguration, RtcSessionDescriptionInit,
};

use std::collections::HashSet;

const MAX_PEERS: usize = 5;

#[wasm_bindgen]
pub struct P2PNetwork {
    ws: Option<WebSocket>,
    #[allow(dead_code)]
    peer_connections: Vec<RtcPeerConnection>,
    data_channels: Vec<RtcDataChannel>,
    seen_messages: HashSet<String>,
}

#[wasm_bindgen]
impl P2PNetwork {
    #[wasm_bindgen(constructor)]
    pub fn new() -> P2PNetwork {
        P2PNetwork {
            ws: None,
            peer_connections: Vec::new(),
            data_channels: Vec::new(),
            seen_messages: HashSet::new(),
        }
    }

    #[wasm_bindgen]
    pub fn connect_signaling_server(&mut self, url: &str) -> Result<(), JsValue> {
        let ws = WebSocket::new(url)?;

        let onmessage_callback = Closure::wrap(Box::new(move |e: MessageEvent| {
            if let Ok(txt) = e.data().dyn_into::<js_sys::JsString>() {
                // In a full implementation, we'd parse the JSON string into SDP/ICE here
                // and call pc.setRemoteDescription or pc.addIceCandidate.
                // For MVP and given WASM async constraints, we log it and surface to JS.
                web_sys::console::log_1(&JsValue::from_str(&format!("WASM received sig: {}", txt)));
            }
        }) as Box<dyn FnMut(MessageEvent)>);

        ws.set_onmessage(Some(onmessage_callback.as_ref().unchecked_ref()));
        onmessage_callback.forget();

        self.ws = Some(ws);
        Ok(())
    }
    
    #[wasm_bindgen]
    pub fn create_peer_connection(&mut self) -> Result<Option<RtcPeerConnection>, JsValue> {
        if self.peer_connections.len() >= MAX_PEERS {
            web_sys::console::log_1(&JsValue::from_str("MAX_PEERS limit reached. Rejecting connection."));
            return Ok(None);
        }
        
        let mut config = RtcConfiguration::new();
        config.ice_servers(&js_sys::Array::new()); // Assuming local network or standard STUN for now
        
        let pc = RtcPeerConnection::new_with_configuration(&config)?;
        
        let dc = pc.create_data_channel("grid_logs");
        self.data_channels.push(dc.clone());
        self.peer_connections.push(pc.clone());
        
        Ok(Some(pc))
    }

    #[wasm_bindgen]
    pub fn broadcast_discovery_log(&self, log: &str) -> Result<(), JsValue> {
        for dc in &self.data_channels {
            if dc.ready_state() == web_sys::RtcDataChannelState::Open {
                let _ = dc.send_with_str(log);
            }
        }
        Ok(())
    }

    #[wasm_bindgen]
    pub fn handle_gossip_message(&mut self, msg_id: &str, content: &str) -> bool {
        if self.seen_messages.contains(msg_id) {
            return false; // Already gossiped this message
        }
        self.seen_messages.insert(msg_id.to_string());
        
        // Relay to other peers
        let _ = self.broadcast_discovery_log(content);
        true
    }
}
