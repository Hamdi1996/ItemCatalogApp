from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem, User


engine = create_engine("postgresql://catalog:catalog@localhost/catalog")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Category Apple
category1 = Category(name = "Apple")

session.add(category1)
session.commit()

item1 = CategoryItem(name = "iPhone X", description = "iPhone X features an all-screen design with a 5.8-inch Super Retina HD display with HDR and True Tone. Designed with the most durable glass ever in a smartphone and a surgical grade stainless steel band. Charges wirelessly. Resists water and dust. 12MP dual cameras with dual optical image stabilization for great low-light photos. TrueDepth camera with Portrait selfies and new Portrait Lighting. Face ID lets you unlock and use Apple Pay with just a glance. Powered by A11 Bionic, the most powerful and smartest chip ever in a smartphone. Supports augmented reality experiences in games and apps. With iPhone X, the next era of iPhone has begun.", os = "iOS", category = category1)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "iPhone 8 Plus", description = "iPhone 8 is a new generation of iPhone. Designed with most durable glass and a stronger aerospace-grade aluminum band. Charges wirelessly. Resists water and dust. 5.5-inch Retina HD display with True Tone. 12MP dual cameras offer improved Portrait mode and new Portrait Lighting. Powered by A11 Bionic, a most powerful smartphone chip. Supports augmented reality experiences in games and apps. With iPhone 8 Plus, intelligence has never looked better.", os = "iOS", category = category1)

session.add(item2)
session.commit()

item3 = CategoryItem(name = "iPhone 8", description = "iPhone 8 is a new generation of iPhone. Designed with most durable glass and a stronger aerospace grade aluminum band. Charges wirelessly. Resists water and dust. 4.7-inch Retina HD display with True Tone. The 12MP camera comes with a new sensor and advanced image signal processor. Powered by A11 Bionic, a most powerful smartphone chip. Supports augmented reality experiences in games and apps. With iPhone 8, intelligence has never looked better.", os = "iOS", category = category1)

session.add(item3)
session.commit()

item4 = CategoryItem(name = "iPhone 7 Plus", description = "iPhone 7 Plus features Dual 12MP cameras for high-resolution zoom and an f/1.8 aperture for great low-light photos and 4K video. Optical image stabilization. A 5.5-inch Retina HD display with wide color and 3D Touch. An A10 Fusion chip for up to 2x faster performance than iPhone 6. Touch ID. Faster LTE. The longest battery life in an iPhone. Immersive stereo sound, splash and water resistant, and iOS 10.", os = "iOS", category = category1)

session.add(item4)
session.commit()

item5 = CategoryItem(name = "iPhone 7", description = "iPhone 7 features an all-new 12MP camera with an f/1.8 aperture for great low-light photos and 4K video. Optical image stabilization. A 4.7-inch Retina HD display with wide color and 3D Touch. An A10 Fusion chip for up to 2x faster performance than iPhone 6. Touch ID. Faster LTE. The longest battery life in an iPhone. Immersive stereo sound, splash and water resistant, and iOS 10.", os = "iOS", category = category1)

session.add(item5)
session.commit()


# Category Samsung
category2 = Category(name = "Samsung")

session.add(category2)
session.commit()

item1 = CategoryItem(name = "Galaxy Note 8", description = "Photos are clear with less blur on the world's first Dual Camera with Optical Image Stabilization on both lenses of the Samsung Galaxy Note8. With the powerful built-in S Pen, take notes without unlocking your screen, handwrite messages and make GIFs. This Samsung Galaxy Note8 comes with a long-lasting 3300mAh battery.", os = "Android", category = category2)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Galaxy S8+", description = "Connect with the world when you make this Samsung Galaxy S8+ smartphone your go-to communication device. Create 4K videos via the gadget's 12MP dual-lens camera array, which comes with an LED flash for low-light conditions. Built around a speedy Qualcomm Snapdragon 835 processor, this Samsung Galaxy S8+ smartphone runs demanding apps and makes multitasking a breeze.", os = "Android", category = category2)

session.add(item2)
session.commit()

item3 = CategoryItem(name = "Galaxy S8", description = "Enjoy UHD video on the road with this advanced Samsung Galaxy S8, which comes with a Super AMOLED 5.8-inch screen. Equipped with active noise-canceling technology, the microphone in this device enables crystal-clear calling while you're on the road. Capture UHD images automatically with the 12MP dual camera in this Samsung Galaxy S8, which has an advanced touch focus feature.", os = "Android", category = category2)

session.add(item3)
session.commit()

item4 = CategoryItem(name = "Galaxy S7 Edge", description = "Work, rest and play with the Samsung Galaxy S7 edge. A massive 5.5-inch Super AMOLED touchscreen goes all the way to the edges of the phone so that you get the maximum area possible to work with. Solid water resistance, great processing and masses of memory round out this Samsung Galaxy S7 edge.", os = "Android", category = category2)

session.add(item4)
session.commit()

item5 = CategoryItem(name = "Galaxy S7", description = "Combine incredible water resistance with a great screen and a powerful processor, and you get the Samsung Galaxy S7. It's built to withstand dunks in water for up to 30 minutes, and then you can wipe it off and get playing with a 5.1-inch touchscreen. The Samsung Galaxy S7 enjoys a quad-core processor for ultra-fast responsiveness.", os = "Android", category = category2)

session.add(item5)
session.commit()


# Category LG
category3 = Category(name = "LG")

session.add(category3)
session.commit()

item1 = CategoryItem(name = "G6", description = "Run the latest apps on this factory-unlocked LG G6 smartphone. Its 4G LTE connectivity provides fast data transfer, and its 32GB of internal storage holds your apps and photos. This LG G6 smartphone is rated IP68 for resistance to water and dust, and its 5.7-inch qHD Plus display delivers brilliant, clear video.", os = "Android", category = category3)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "V20", description = "Record crisp, clear content - even when you're on the move. Steady Record 2.0 allows you to capture sharp, smooth video by minimizing the effects of unintentional hand shaking. Get the best sound with the first smartphone to include Quad DAC for cleaner playback. Stream sound in the highest quality heard yet.", os = "Android", category = category3)

session.add(item2)
session.commit()

item3 = CategoryItem(name = "G5", description = "Work and play all in one place with this unlocked LG G5 smartphone, featuring a 5.3-inch screen for easy viewing. The sleek comfortable body fits easily in your hand, and dual rear-facing cameras make photography fun. This LG G5 smartphone has Daylight mode, letting you easily view your screen even in bright sunshine.", os = "Android", category = category3)

session.add(item3)
session.commit()

item4 = CategoryItem(name = "G4", description = "Quickly communicate with friends and family by using this LG G4 smartphone. It includes 32 GB of storage, a microSD card slot and plenty of memory so that you can take full advantage of the smartphone's online and social media capabilities. The powerful Android operating system ensures you stay connected with everyone when using this LG G4 smartphone.", os = "Android", category = category3)

session.add(item4)
session.commit()


# Category Google
category4 = Category(name = "Google")

session.add(category4)
session.commit()

item1 = CategoryItem(name = "Pixel", description = "Bring the power of Google directly to your fingertips with the Google Pixel. A large 32GB of storage keep data secure, while unlimited cloud storage transfers data as needed, and it's completely automatic. The large 5-inch screen is protected by Corning Gorilla Glass 4 to ensure the Google Pixel remains scratch-free.", os = "Android", category = category4)

session.add(item1)
session.commit()

item2 = CategoryItem(name = "Pixel XL", description = "Add high-end performance to your everyday life with the Google Pixel XL. A quad-core processor, a 5.5-inch LED screen and 32GB of memory ensure this phone is able to handle daily life, and Corning Gorilla Glass 4 protects the screen. Easy cloud storage ensures you never run out of space on the Google Pixel XL.", os = "Android", category = category4)

session.add(item2)
session.commit()


print "All Items have been added to the database."
