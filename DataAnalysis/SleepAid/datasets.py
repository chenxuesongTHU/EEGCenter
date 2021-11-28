#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   datasets.py
@Time        :   2021/11/9 8:11 下午
@Author      :   Xuesong Chen
@Description :
"""

# dodo
dodo_filename_list = [
    'b2d3ccdd-395c-5dd2-81d9-252bcfc0c337',
    '52fbe46b-206c-584a-9f4f-1eb308e07bac',
    '7f5237b1-2196-5c8a-9543-a5aa70210ef4',
    '3dd35e7b-d7e2-516d-8a85-e0d58a59569f',
    '039ce8ad-a7fa-5272-a3e3-1f4bfebdd087',
    '4e3c4ac4-69e2-5347-a3b0-662c204d259d',
    'f66bc75e-778b-5037-af86-b5275cd4c79f',
    '30e8a05b-4cf1-5aa8-9ef7-28d6e2949ad5',
    'fc10ee0b-b863-511b-bce8-4dfa7af8ac3a',
    '02fb158a-a658-51ee-89cf-1e1dc2ebfde1',
    '32556393-bb57-560a-99e8-e09885219647',
    'd5181c33-a43b-5dfe-8ad7-0337facb092a',
    '6e2aa933-c51c-5a31-8c7b-83da8d076a12',
    'cc3b4b63-4a6f-5f28-ac7e-62f83c271449',
    'a6254c8a-f1b2-5736-b601-18245dd5e0a5',
    '5b94ec8a-c34d-5e45-84d1-bec2ea965609',
    '47f45aa2-31c4-595b-bdb6-f1348bba062b',
    'e72505f1-21be-5d66-b620-cfcfa2d754bc',
    '100df108-eb57-5eaa-a413-f7e4436a7895',
    'e8ec8ec4-dc48-50ce-985a-a06d87861030',
    'c11c730f-0b6b-580b-af31-d8f0ebbbdfce',
    'e6b7cbef-4c9d-5541-82e8-04810de0fb60',
    'e59c45e0-0c0c-565f-84a9-6cf0ec5ef6c1',
    'c03e27b0-4cb5-584f-aaea-8f1e1ed6513c',
    'b3706da5-748b-5dd1-a552-f57e4456cdf6',
    '90aef91a-252f-5ccc-a82e-78ea7ee9ca1f',
    'a35a118e-e65e-5928-92a9-4354a6a0f4ce',
    # '5d8e93a5-d26a-436d-bc2c-e9527dc92cbf',
    '40e25dd4-6087-5747-b9c2-4838ada86b15',
    '22bea84c-5d23-5e49-bc2d-9764f883955b',
    'a79d1f0e-c133-5aa0-8268-cdcc05825f0f',
    'ad47bc12-199c-5294-9cb8-4351bbbf7b5e',
    'a65a9e69-cddf-5711-9a97-de8bfdeb08cc',
    'aadc9e0c-b7c3-5a47-851d-f21971d10935',
    '130f3f52-7d0a-551e-af61-2ee75455e5c9',
    '16450f5a-9b65-5536-85e1-93816c8b89eb',
    'c985916d-46a5-5c3e-9d50-a5a91f460bac',
    'eb95076c-c470-56a4-b788-ace310f061c6',
    '0416d51f-5d69-5326-b74a-a2e31a96a1ef',
    '83c1394e-9c69-5c11-9102-9ff8d59b1cfd',
    '2159377e-ebf3-5565-9014-1e2ae69dc1d2',
    'cebd3520-4e77-5222-a614-d2888e6afc2b',
    'c31a47f9-e400-5841-a22b-521c81042603',
    'b3534fa3-7676-50dc-8412-07f0eff4f7a9',
    '03341d0d-5927-5838-8a5f-1b8ef39d8f57',
    '730aba3b-e310-5be0-9eed-7c3123466834',
    'c8110476-594c-533d-95bd-86147fccc987',
    '79e8a04e-0fdd-53ae-bedc-d49d08e29103',
    '2d01dc34-f36c-562e-b24a-d20dc798fdfc',
    'a0c91989-530f-5117-80c1-2488dbed683c',
    '742f1592-627c-54eb-bbb5-ccd55ffae33a',
    '18482adf-1144-54ca-9e35-27f65c43a105',
    '2e865ca9-e20f-5a6f-bd25-45d28cc9eab9',
    '6a7503ac-ab3a-5d5b-b474-4b0fe37748dd',
    '5ddbc68c-1283-5c27-952b-d7f102291bc2',
    '4b72b905-5521-5c57-b666-e20ff9bb195f',
]

# dodh
dodh_filename_list = [
    '119f9726-eb4c-5a0e-a7bb-9e15256149a1',
    '7d778801-88e7-5086-ad1d-70f31a371876',
    'a4568951-bf87-5bbc-bc4f-28e93c360be6',
    '769df255-2284-50b3-8917-2155c759fbbd',
    '25a6b2b0-4d09-561b-82c6-f09bb271d3be',
    'aa160c78-6da3-5e05-8fc9-d6c13e9f97e0',
    '67fa8e29-6f4d-530e-9422-bbc3aca86ed0',
    'd3cadb78-cb8c-5a6e-885c-392e457c68b1',
    '64959ac4-53b5-5868-a845-c7476e9fdf7b',
    '1da3544e-dc5c-5795-adc3-f5068959211f',
    'b5d5785d-87ee-5078-b9b9-aac6abd4d8de',
    '14c012bd-65b0-56f5-bc74-2dffcea69837',
    '095d6e40-5f19-55b6-a0ec-6e0ad3793da0',
    '37d0da97-9ae8-5413-b889-4e843ff35488',
    'a30245e3-4a71-565f-9636-92e7d2e825fc',
    '7ab8ff5f-a77f-567d-9882-f8bee0c3c9bf',
    '5bf0f969-304c-581e-949c-50c108f62846',
    '0d79f4b1-e74f-5e87-8e42-f9dd7112ada5',
    'f2a69bdc-ed51-5e3f-b102-6b3f7d392be0',
    '3e842aa8-bcd9-521e-93a2-72124233fe2c',
    'bb474ab0-c2ce-573b-8acd-ef86b0fa26a2',
    '18ede714-aba3-5ad8-bb1a-18fc9b1c4192',
    '844f68ba-265e-53e6-bf47-6c85d1804a7b',
    'a25b2296-343b-53f6-8792-ada2669d466e',
    '1fa6c401-d819-50f5-8146-a0bb9e2b2516',
]

# ChineseMedicine
ChineseMedicine_filename_list = [
    '1',
    '40'
]

ChineseMedicine_user_info = {
    'health': [79, 80, 81, 82, 83, 85, 86, 87, 88, 89, 90],
    'insomnia': {
        'ta-VNS': {
            'before': [1, 4, 5, 9, 12, 14, 20, 24, 26, 30, 32, 34, 36, 38],     # 22
            'after': [40, 43, 44, 48, 51, 53, 59, 63, 65, 69, 71, 73, 75, 77],  # 61
        },
        'tn-VNS': {
            'before': [8, 10, 16, 17, 21, 23, 25, 27, 31, 35],              # 2
            'after': [47, 49, 55, 56, 60, 62, 64, 66, 70, 74],              # 41-2
        },
    },
}
