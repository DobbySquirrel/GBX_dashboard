import pandas as pd

# Geo data provided
geo_items = {
    'Latitude': [22.894559689319834, 22.886376973309183],
    'Longitude': [113.47484770222422, 113.4830306533438],
    'X': [-1.4901161193847656e-7, 1142.998168796301],
    'Y': [0, 1244.0001220703125]
}

# Latitude and Longitude coordinates to convert
coords =[
                  [
            113.47966750732246,
            22.894535821788693
          ],
          [
            113.47937179433819,
            22.89447528456192
          ]
        ]


# coords = [
#     [113.47831684233165, 22.890465102808733],
#     [113.47891349762205, 22.89002321150423],
#     [113.47936976343374, 22.89063754780554],
#     [113.4796388432714, 22.891273436837054],
#     [113.47987282573825, 22.89201709989004],
#     [113.48016530382245, 22.892534428306178],
#     [113.48044608278457, 22.892965533811903],
#     [113.47935806430928, 22.893569079220214],
#     [113.47952185203684, 22.894194176991164]
# ]
# coords = [
#             [
#             113.47872088332235,
#             22.892061020308077
#           ],
#           [
#             113.47953830802487,
#             22.894216859923475
#           ]
# ]

# Convert to DataFrame for easier manipulation
geo_df = pd.DataFrame(geo_items)
coords_df = pd.DataFrame(coords, columns=['Longitude', 'Latitude'])

# Calculate scaling factors (linear transformation)
delta_lat = geo_df['Latitude'][1] - geo_df['Latitude'][0]
delta_lon = geo_df['Longitude'][1] - geo_df['Longitude'][0]
delta_x = geo_df['X'][1] - geo_df['X'][0]
delta_y = geo_df['Y'][1] - geo_df['Y'][0]

scale_x = delta_x / delta_lon
scale_y = delta_y / delta_lat

# Calculate the offsets (anchor point transformation)
offset_x = geo_df['X'][0] - geo_df['Longitude'][0] * scale_x
offset_y = geo_df['Y'][0] - geo_df['Latitude'][0] * scale_y

# Apply transformation to coords data
coords_df['X'] = coords_df['Longitude'] * scale_x + offset_x
coords_df['Y'] = coords_df['Latitude'] * scale_y + offset_y

# Prepare the output in the specified format
output = coords_df[['X', 'Y']].values.tolist()
print(output)
