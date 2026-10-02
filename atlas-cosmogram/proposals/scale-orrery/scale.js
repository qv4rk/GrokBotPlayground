// Sizes and the two scale modes.
//
// The Scale Orrery's "true" mode multiplied radii by 0.1 and kept the Sun at a
// fixed 3 units, so Earth came out about 160x too large against its orbit and
// the Sun only 2.7x Jupiter's radius (it is 9.7x). Here both modes start from
// one unit for distance and radius, and the visible mode states its one lie.

export const AU_KM = 149597870.7;

// Scene units per AU. Matches The Scale Orrery's AU_SCALE.
export const UNITS_PER_AU = 15;

// Equatorial radii, km (IAU WGCCRE 2015 / NASA fact sheets).
export const RADIUS_KM = {
  sun: 695700,
  mercury: 2439.7,
  venus: 6051.8,
  earth: 6378.137,
  mars: 3396.2,
  jupiter: 71492,
  saturn: 60268,
  uranus: 25559,
  neptune: 24764
};

// Saturn's main rings, km from Saturn's centre (inner C ring to outer A ring).
export const SATURN_RING_KM = { inner: 74658, outer: 136775 };

// Saturn's north pole, IAU J2000 RA/Dec in degrees. Used only to tilt the ring.
export const SATURN_POLE = { ra: 40.589, dec: 83.537 };

export const MODES = {
  // One factor for every planet, so planets stay true to each other.
  // The Sun gets its own smaller factor so it does not swallow Mercury's orbit.
  visible: { planet: 1000, sun: 20, label: 'Visible: planets ×1000, Sun ×20' },
  // Same unit for distance and radius. Nothing enlarged.
  true: { planet: 1, sun: 1, label: 'True: radii and distances on one scale' }
};

export function kmToUnits(km) {
  return (km / AU_KM) * UNITS_PER_AU;
}

export function radiusUnits(body, mode) {
  const m = MODES[mode] || MODES.visible;
  return kmToUnits(RADIUS_KM[body]) * (body === 'sun' ? m.sun : m.planet);
}
