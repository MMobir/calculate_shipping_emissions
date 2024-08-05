# Container Shipping Methods

**Mandatory input:**

- `container_ship`

A container transport is either refrigerated or "dry" (not refrigerated). Dry transports result in lower emissions.

**Optional input:**

Container transport emissions vary per trade lane. When a trade lane is not given we'll use an industry-wide average. Providing an `aggregated_*` trade lane group will result in an a more accurate estimate. Providing an `disaggregated_*` trade lane will result in the best estimate precision.

The identifiers are kept relatively short for brevity: Mediterranean includes Black Sea and South America includes Central America.

The trade lanes are bidirectional, for example `disaggregated_asia_to_africa` covers both Asia to Africa and Africa to Asia.

- aggregated_panama_trade
- aggregated_transatlantic
- aggregated_transsuez
- aggregated_transpacific
- aggregated_other
- disaggregated_asia_to_africa
- disaggregated_asia_to_mediterranean
- disaggregated_asia_to_middle_east
- disaggregated_asia_to_north_america_east
- disaggregated_asia_to_north_america_west
- disaggregated_asia_to_north_europe
- disaggregated_asia_to_oceania
- disaggregated_asia_to_south_america
- disaggregated_europe_to_africa
- disaggregated_europe_to_south_america
- disaggregated_europe_to_middle_east
- disaggregated_europe_to_oceania
- disaggregated_mediterranean_to_north_america_east
- disaggregated_mediterranean_to_north_america_west
- disaggregated_north_america_to_africa
- disaggregated_north_america_to_oceania
- disaggregated_north_america_to_south_america
- disaggregated_north_america_to_middle_east
- disaggregated_north_europe_to_north_america_east
- disaggregated_north_europe_to_north_america_west
- disaggregated_south_america_to_africa
- disaggregated_intra_africa
- disaggregated_intra_north_america
- disaggregated_intra_south_america
- disaggregated_se_asia_to_ne_asia
- disaggregated_intra_ne_asia
- disaggregated_intra_se_asia
- disaggregated_north_europe_to_mediterranean
- disaggregated_intra_mediterranean
- disaggregated_intra_north_europe
- disaggregated_intra_middle_east
- disaggregated_other