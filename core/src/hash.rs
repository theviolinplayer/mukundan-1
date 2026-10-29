use ark_bn254::Fr;
use ark_ff::{BigInteger, PrimeField};
use light_poseidon::{Poseidon, PoseidonHasher};

pub fn poseidon_hash_2(left: Fr, right: Fr) -> Fr {
    let mut hasher = Poseidon::<Fr>::new_circom(2).unwrap();
    hasher.hash(&[left, right]).unwrap()
}

pub fn poseidon_hash_3(a: Fr, b: Fr, c: Fr) -> Fr {
    let mut hasher = Poseidon::<Fr>::new_circom(3).unwrap();
    hasher.hash(&[a, b, c]).unwrap()
}

pub fn poseidon_hash_5(a: Fr, b: Fr, c: Fr, d: Fr, e: Fr) -> Fr {
    let mut hasher = Poseidon::<Fr>::new_circom(5).unwrap();
    hasher.hash(&[a, b, c, d, e]).unwrap()
}

pub fn fr_from_u8_array(arr: &[u8; 32]) -> Fr {
    Fr::from_le_bytes_mod_order(arr)
}

pub fn u8_array_from_fr(fr: Fr) -> [u8; 32] {
    let mut arr = [0u8; 32];
    let bytes = fr.into_bigint().to_bytes_le();
    let len = bytes.len().min(32);
    arr[..len].copy_from_slice(&bytes[..len]);
    arr
}
