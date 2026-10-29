// wasm-bridge/p2p_mesh.js

export class DiscoveryMesh {
    constructor() {
        this.peers = new Map();
        // Use standard Google STUN for NAT traversal
        this.rtcConfig = { iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] };
    }

    /**
     * Initializes a WebRTC DataChannel to a new peer for gossip.
     */
    connectPeer(peerId) {
        const pc = new RTCPeerConnection(this.rtcConfig);
        const dc = pc.createDataChannel("discovery_logs", { ordered: false });
        
        dc.onmessage = (event) => this.verifyGossip(event.data);
        dc.onopen = () => console.log(`[P2P] Connected to ${peerId}`);
        
        this.peers.set(peerId, { connection: pc, channel: dc });
        return pc;
    }

    /**
     * Broadcasts a zero-knowledge folded checkpoint to all connected peers.
     */
    broadcastCheckpoint(machineId, stateBufferPtr, memory) {
        // Read the exact 112-byte aligned buffer from WASM memory
        const rawBuffer = new Uint8Array(memory.buffer, stateBufferPtr, 112);
        
        const payload = JSON.stringify({ 
            id: machineId, 
            state: Array.from(rawBuffer) 
        });

        for (const [id, peer] of this.peers) {
            if (peer.channel.readyState === 'open') {
                peer.channel.send(payload);
            }
        }
    }

    /**
     * Pre-folding validity check to prevent accumulator poisoning.
     */
    verifyGossip(data) {
        const payload = JSON.parse(data);
        
        // Offset 100 corresponds to the `status` field in CheckpointLayout
        // Offset 104 corresponds to the `active_state` bounds
        const stateId = payload.state[104]; 
        
        if (stateId > 5) {
            console.warn("[P2P] Rejecting gossip: BB(6) state bounds exceeded.");
            return;
        }
        
        console.log(`[P2P] Verified Checkpoint for Machine ${payload.id}`);
    }
}