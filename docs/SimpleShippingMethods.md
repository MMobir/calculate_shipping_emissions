# Simple Shipping Methods

## Available methods

**Sea**

- inland_waterway_motor_vessel_small
- inland_waterway_motor_vessel_medium
- inland_waterway_motor_vessel_large
- inland_waterway_coupled_convoy
- inland_waterway_pushed_convoy_small
- inland_waterway_pushed_convoy_medium
- inland_waterway_pushed_convoy_large
- inland_waterway_tanker
- inland_waterway_container_vessel_medium
- inland_waterway_container_vessel_large
- inland_waterway_container_vessel_convoy

**Rail**

- diesel_freight_train
- electric_freight_train

**Road**

- diesel_truck
- truck_generic_van
- truck_generic_urban
- truck_generic_mgv
- truck_generic_hgv
- truck_rigid_7_5t
- truck_rigid_12t
- truck_rigid_20t
- truck_rigid_26t
- truck_rigid_32t
- truck_articulated_34t
- truck_articulated_40t
- truck_articulated_44t
- truck_articulated_60t
- truck_articulated_72t
- truck_na_van
- truck_na_general
- truck_na_auto_carrier
- truck_na_dray
- truck_na_expedited
- truck_na_flatbed
- truck_na_heavy_bulk
- truck_na_dry_van_ltl
- truck_na_dry_van_tl
- truck_na_mixed
- truck_na_moving
- truck_na_package
- truck_na_refrigerated
- truck_na_specialized
- truck_na_tanker

**Air**

- cargo_plane
- passenger_plane
- plane

### **Vessel sizes**

- `inland_waterway_motor_vessel_*`:
    - `small` – less than 80 m / 1000 t
    - `medium` – 85-110 m (1000-2000 t)
    - `large` – 135 m (2000-3000 t)
- `inland_waterway_coupled_convoy` – 163-185 m
- `inland_waterway_pushed_convoy_*`:
    - `small` – 2 barges
    - `medium` – 4-5 barges
    - `large` – 6 barges
- `inland_waterway_container_vessel_medium` – 110 m
- `inland_waterway_container_vessel_large` – 135 m

### **Road transport**

As far as road transport is concerned we support a variety of trucks (the `truck_*` methods). Our emission estimates assume diesel fuel and average load and empty running characteristics at the moment, unless a specific type says otherwise.

**Regional differences**

Truck types in North America and the rest of the world are categorized differently, therefore they're available here as distinct shipping methods. The North America trucks are prefixed with `truck_na_` while for the rest of the world it's just `truck_`.

**Truck sizes**

- Vans (`truck_generic_van`, `truck_na_van`) are under 3.5 tonnes GVW (Gross Vehicle Weight).
- `truck_generic_urban` is between 3.5 and 7.5 tonnes GVW
- `truck_generic_mgv` is between 7.5 and 20 tonnes
- `truck_generic_hgv` is above 20 tonnes GVW

For other truck types the GVW is either in the method name (like `truck_rigid_7_5t` which is up to 7.5 tonnes) or is not specified.

**Choosing the right truck type**

The are significant differences in emissions of different truck types. The more precisely you can declare what kind of truck you use, the better.

If you only know a rough size of the truck you'll do well can choose one of the `truck_generic_*` types if outside North America.