from datetime import date
from app import app, db
from models import Admin, DeliveryGuy, Courier

with app.app_context():
    # Drop all tables and create them again
    db.drop_all()
    db.create_all()


    ad1 = Admin(first_name="John", last_name="Doe", city="Nairobi", state="Kenya", branch_code="57hg", profile_pic="https://media.istockphoto.com/id/1327592506/vector/default-avatar-photo-placeholder-icon-grey-profile-picture-business-man.jpg?s=1024x1024&w=is&k=20&c=er-yFBCv5wYO_curZ-MILgW0ECSjt0DDg5OlwpsAgZM=")
    ad2 = Admin(first_name="Jane", last_name="Doe", city="Nairobi", state="Kenya", branch_code="57hg", profile_pic="https://media.istockphoto.com/id/1327592506/vector/default-avatar-photo-placeholder-icon-grey-profile-picture-business-man.jpg?s=1024x1024&w=is&k=20&c=er-yFBCv5wYO_curZ-MILgW0ECSjt0DDg5OlwpsAgZM=")

    db.session.add_all([ad1,ad2])
    db.session.commit()

    print("Database seeded successfully!")


  # Create Couriers
c1 = Courier(
    name="Speedy Couriers",
    address="123 Oak Road",
    city="Nairobi",
    state="Kenya",
    phone_number="5551112233",
    email="support@speedycouriers.com"
)



c2 = Courier(
    name="Rapid Delivery",
    address="456 Birch Lane",
    city="Nairobi",
    state="Kenya",
    phone_number="5554445566",
    email="hello@rapiddelivery.com"
)

c3 = Courier(
    name="OnTime Logistics",
    address="789 Cedar Street",
    city="Mombasa",
    state="Kenya",
    phone_number="5557778899",
    email="contact@ontimelogistics.com"
)

c4 = Courier(
    name="GoDeliver",
    address="101 Elm Way",
    city="Nairobi",
    state="Kenya",
    phone_number="5552223344",
    email="info@godeliver.com"
)

c5 = Courier(
    name="QuickShip",
    address="234 Pinecrest Drive",
    city="Nairobi",
    state="Kenya",
    phone_number="5553334455",
    email="service@quickship.com"
)

c6 = Courier(
    name="Cargo Express",
    address="345 Maple Street",
    city="Mombasa",
    state="Kenya",
    phone_number="5558889900",
    email="info@cargoexpress.com"
)

c7 = Courier(
    name="Parcel Masters",
    address="456 Willow Avenue",
    city="Nairobi",
    state="Kenya",
    phone_number="5555556677",
    email="support@parcelmasters.com"
)

c8 = Courier(
    name="NextDay Delivery",
    address="567 Fir Boulevard",
    city="Mombasa",
    state="Kenya",
    phone_number="5556667788",
    email="contact@nextdaydelivery.com"
)

c9 = Courier(
    name="FastDelivery Inc.",
    address="789 Pine Street",
    city="Nairobi",
    state="Kenya",
    phone_number="5551234567",
    email="contact@fastdelivery.com"
)

c10 = Courier(
    name="Express Transport",
    address="101 Maple Avenue",
    city="Mombasa",
    state="Kenya",
    phone_number="5559876543",
    email="info@expresstransport.com"
)

# Seed the database
with app.app_context():
    db.create_all()  # Ensure all tables are created
    db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])
    db.session.commit()
    print("Database seeded!")
    

    # Create DeliveryGuys
    delivery_guys = [
        DeliveryGuy(
            first_name="Alex", second_name="Smith", address="123 Main Street", city="Nairobi",
            state="Kenya", phone_number="+254701234567", mode="Bike",
            live_location="-1.2921, 36.8219", profile_picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAvSmmOy18YNF05qTMOohuxHxHctENUSwxFA&s"
        ),
        DeliveryGuy(
            first_name="Emily", second_name="Johnson", address="456 Elm Street", city="Nairobi",
            state="Kenya", phone_number="+254701234568", mode="Car",
            live_location="-1.2950, 36.8179", profile_picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-kd2ihsLPqFVly2PC_SJtnvEj4HBT5tk27Q&s"
        
        ),
        DeliveryGuy(
            first_name="Jackson", second_name="Martin", address="1616 Juniper Street", city="Nairobi",
            state="Kenya", phone_number="+254701234585", mode="Bike",
            live_location="-1.3120, 36.8340", profile_picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5Ay0roe-tiTfkNLJQMuRD0VGuZtOd7axkpgSXacvKvqMIJ0ZY0APNWzPAUA&s"
        ),
        DeliveryGuy(
            first_name="Isabella", second_name="Lee", address="1717 Oakwood Street", city="Nairobi",
            state="Kenya", phone_number="+254701234586", mode="Car",
            live_location="-1.3130, 36.8350", profile_picture="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBw8QDw8PDw8PEA8QEBAWEBAQDw8QFhAQFhUWFhUVFRUYHiggGBolHRUWITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGhAQGislICUtLS8uLS0tLS0tLS0tLS0tLS0tLS0rLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIALcBEwMBEQACEQEDEQH/xAAcAAEAAgMBAQEAAAAAAAAAAAAAAQMCBQcEBgj/xAA/EAACAQIDBgQCCAMHBQEAAAAAAQIDEQQSIQUGMUFRYRMicYEHoRQyQlKRscHRM3LwI1NikrLh8UNzgqLCJP/EABoBAQACAwEAAAAAAAAAAAAAAAABAwIEBQb/xAAwEQEAAgIBAwMCBQMEAwAAAAAAAQIDEQQSITEFQVETYSIyQpHRcYGxFVKhwRQjkv/aAAwDAQACEQMRAD8A7WQJAAAAAAAAAAAEAAAAABAAAAAgAAAAAIAAAAACAFgIaAxaAxsB6gAAAAAAAAAAAAAAAEBIEAACAAAAAAgAAAAAAACAAEAQ0BjYD0AAJAAAIAAAAAAACQABAGl3r24sHh5TVnWlpSi/vfefZGzxePOa+vb3a3Jzxipv39nLqu8eOk7vF17t/ZqSgvZRsl6HcrxMMfphxrcnLP6pYw2/jU7rF4i//em1+DZM8XFP6YYxyMseLS+/3O3tWJtQxDSxH2ZaJVf2l258jkcvifTnqr4dXi8r6kdNvL640G8gJAAQAAIAAAAAABAACGBAFwEgAAACAAAAAAAAkAAV16sYQlOTtGEW5PokrsmsTadQi0xEblyDeXaksTWc58NMsb/VjyX9dT0fGwxipqHA5GSclty1CV+Bs7a2kWS4tfihs0rVW0s0Xwas0+a7oqvG1lJ07Hujtj6XhY1JO9SDcKv8ys7+6afuzz3IxfTvqPDvcfL9Sm58t0ULwAACAJAgAgAACQAEAEAQBcAAAAAEAAAAAACQAAA+N+KW2/omCVoucq1RRUU0rpeZ68uRfx71x267eynNS146K+7j2ytu1MRWdJ0ZXtoqX9plS4uTsvkb1PVaxP441DUt6XaY1Sdyux22KNG6nGs2uKVKb+b0+Zs/6ng1uJa3+mZ96mNNe94Kk1ehQSi+EpvN8o6fNmnl9WnxWv7tvF6PE97W/Z4sTtnHx8zcMq+z4Uf1NePUskz302LemY4jtt0P4Tb9UlJ4bEJU/HnHJUT8qqcEpJ8L6K9y3PH1o648wow/+qemfEuymg3kAAAAAAAAEACAJAAQAQBaAAAAAEAAAAAACQAAA+X3mhTxFeOGnCNSNKhKo4WhKTnUl4cLKWi0jUT/AJl0KM8zERps8aI3O3x3w/3QlgZ4nxXGUpOMYvi8nHV+5Rkv1tnFj6Nrd89gYhrxKEqajb6sqbbb/mT/AEMaz0/mZWib/laXZW7/AJKlSpSUWlK1o5c6XByjwQm/xLKmPXmHy+KhHETyqcqUHKMb+ErRcr5c0n1yvh+pfXcd2te3VOn1uH+DtaNClOliYKvKN6tGrFxjFt3SjON2rLR3T16HRw5+iNS5eXD1TuHXsBTnCjShVkp1I04RqTX25qKUpe7uyi07ncLo7QvISAAJAAAAAAAAAAAQgCwCQAEAAAAAAABIAAAQB8tvbTeHmtp0455UqM6dalmy+JRvnTTtpKLTt1zNFWWu+63FbU6Y7OxirUoV1HL4kIzte9rpO1+Zp27S366mHj2nthupHDZoUU1d1KvDrljycrDc27LK16Z2jGY6lRg895U8jtUpuMlJ9LLmR067M9z5l85snB4eq4KMfN4kYq611aszKu+pVfp6Jl1hs6DkgEASAAAAAEgAAAAAABABmAAAAAAAACQAAAAAIYHzHxCm1s/EW5xt80V5Z1CzFG7NHsSq6eDwua9vBp3fTQ07TEt6kTEN1h8PCcJa3cne6dmna10zGkLZvqYfKbybNqyU4rIr6eNBZanrpxfrczi0bX2mvT23H232bncXYGRQrzzNQXklNtupN8Za8lwRdhpO+qXN5GWNdMPtrmy0y4C4C4E3AAAJAAAJAAAAAAEMwAAAAAAAkAAAAEAAIA+X3+o1KuG8GlHNKpUipapJQWrbfJFGedQv48blVhcLGOHhSeqjkgtOPJmnvcN6I00u1KVbDXlRk7fdf6CJ+U/0ePYW0Z4jFUadZJQcm53ejyxbs+2hdjis2VZsluiXTU1ZWtblbgbrneS5AXAXJEgAJAkABIAABIAAAABDMAAAAAASAAAEAANbtzbVHB089Vtt6Qpxtmm+3Rdy/BgvmtqrX5HIpgr1WfGVPiRUzaYaGTo5yv8A5uHyOjHpca72cqfWJ32q+e2vvbjMRJ3rSpwfCnSbgku9tX7tm5h4WLHHjc/do5+fmyT51HxC/dXbjpS8GopThVmrNXlJVHZe6ehpeqenxmr9SvaYj/hv+j+pThv9K+5i0/tLo0cJeMVezTvwueXiu4esnJqZazbez3kvKas2la3VmNq6WY8kW7PicTgZSm8sfKtOHFEVtpnau3yM6uIwlSdOhiK1KObVUq1SmmuX1WuCsj1fFxRkw1taO+nkOVmnFnvWs+JbTZ+9206VsuLqzS5Vcta/vNNmzPCxT5hq/wDnZY931Wy/iVUVo4mhGeus6Tyu3XK9G/dGtk9Mj9EtjH6rMfnj9nQNm7QpYilGtRmpwlz4NPmmuTOXkx2x26bOtjy1yV6qz2eq5WsSBJIkABIEgAAEgAAAIZgAAAJAAACAAACuvWjThKc3lhCLcn0S1ZlWs2mIhja0VibT4hxjejaksRialV3tooQbvliuXqem42CMWOIeS5eec2WbezTqV+BstadxK7CYSpWmqdKEpzf2V+b6LuVZctMVeq86hbhw5M1+ikbl0HdbdL6PJVq7jOql5Ix+rTb4u74y/I81z/VJzx9PHGq/5eo9P9Kjjz9TJO7f4fXR0OXHZ1p7tbvDWlHDVZRUfLG7zdFrp30Guq0V+ZZRqkTb4hyLF714qqssVlT45IZfm9Uemxel8ak7iu5+7zWX1XlXjU3iI+zStSc9eXH1fc6Fa99OXNu2/l6YwLdKZsxaMRstg7fr4Kqp0peV2z039Wa7rr3NfPgpljVmxgzXwz1Vn+zsO7+3aONpeJSdpL69NtZoPv1XRnBz4LYbal6Lj8iuau6/s2iZQ2GQEkiQAEgAJAASAAgCwAEAACAASAAAAD4n4h7YyqOFg9WlUq+ifkj7tXfojq+m8fc/Un+kOL6tyunWKP6z/wBOZVX/AL/udxwK93t3f2JXxU2oK1NS81Vryrql959kaHL5+PjR37z8OpxfTsnKmJjtX3l1HYmx6OFhlprV2zTf1pvu/wBDyfJ5WTkX6rz/AG9oes43Fx8anRjj+/vKzHbZoUdJz17a29WUxO+0d5bHR23PaPu8K3twn94vct+jm/2T+yv6uH/fH7tRvXvFQqYSpCGspx0d+CubPBw3nkU3We0tfnZaV419WjvDnSZ694rfyxpwt7k1hFp2yk9BLGFEpGG1sQqk9TH3Zx4e7ZW0auHqRq0ZOM48Gua5prmuxF8dclem0FL2x26qzqXVN2996GIShXcaFbu7Qm/8Mnw9H+LONyOBfH3p3h2+N6jTJ+G/af8Ah9YmaDpJRAkkZAAJAASAAAALAgAgAACQAAAgDCtVUIynJ2jGLcn0SV2TWJmdQxtaKxMy43trGTxWJqTjFynVekYptqK0ilbtY9PirTj4o6p1EPI5rX5OeeiNzLb7D3McmqmL4cVRT/1yX5L8Tic31rf4MH7/AMO/wfQ4rq/I/wDn+X2tGlCnFRhFRjFWUYpJJdkcC1ptO7TuXoorERqIa3bW2IUYNt62IrW2S0UpHeWczXHWb3nUQ5htXasq822/Lyiew4Hp9ONXc97T5n+Hi/UfUb8q+o7VjxH8tbOodCZc6KsM5jtnqGUJdPwJiWMx8rVIy2r0qqTMJllWrzzmVzK6IYRepMSmY7Lkn1MmG2cZvrcljNdupbq4/EUMNSjUbqLLfLLjFN3ST9OR43l82J5Fpr+V7fh8Ca8asWn8T67A46nWV4PVcYvRx9UZ0yVvG4YZMVqTqXqRmrZEiQAEgSAAAAMwgCQAAAAQAAAaLemUp01h4Sy+JrNrV5VwSXf9O5EcqOPaLa3KZ4c8mk13qGv2Ts2lQjaEdXxk9ZS9WafI5mXk23kn+3s3ONwcPFr044/rPvLY5uvA19tjTR7e2/CjFpPUzx475bRSkd5RkvTDSb3ntDmO2NsVK07yby30R63g8CnFjc97fP8ADyPP9Qvy56Y7V+P5a6dbmb82c2KKnXTMOpn9PSY1SYsTVZ4hO2OlsKhltXarGtUK720mldvHm0b/AAKt9ttjXfSKNTUypYtXs9kIc2y6IUTP2fSbubr18VCVeCjkhJKEZtx8Vr62V8NNOOl32OX6pyLVp9PHPef8Or6Vx62yfUyR2j/L6zAYicZ+HUhKE1a8JKzt1XVHkJrNZ1L2kWraNw2c4yhJVabtJfg10fYml5pO4Y3pF69Mvodn42NaGaOj4SjzjLodTHki8bhycmOcdtS9SM1bJEiQJAASAAAZgAAAABAAABDYHzVSWacqj4yenZckcnJbqtMuxjp01iGNTExirtmHUy6dvn9ubxKEJPMopJ3dzOlLXnUMb2rjjcuW7U29OvVzJvw+S692eq4HHrx437z5eW9Q5E8mde0KXWzHT6tuVFNKnMrmWcVYNPiRpltnCVyYYzDNGUMVsZuxlthMJqy8rfYqySyxR3eatO0Uuib/AGMMk6jSzHXc7Z7F2ZXxdVUaEHKfN65YJ/anL7KKbZa0jcy2K4rXnUQ6Ju78Nsk5yx1SNSGVZIUZ1F5r6uUmk7JLguN+xp35tv0NynCr+vu6NhqUKcI04RUYQSUYxVkkuSNK1ptO5btaxWNQr2jgo1o6+WcdYT+6+/bqinJji8aldiyTSdw1WEnNpxcG7Nq8bOL7qXCxz+iYnTpfVrrb0YOhOnNzjNRurONs11y6Wa9yzHM457KcsxkjUw3eFq5o68U2n+a+TRvY7dVdtG9emV6ZYwZICQJAAAAFgAAEIABIAAAVYiLlCcVxcZJerWhFo3Ewms6mJfH4nF5IXk7afM5ExLtxMeWmjVq4qp4dCDnJ8eUYrrJ8kZ48U2lVkzRWHr3r3YpUNj4+Uo+PX8HNKeqyZJRl5FyStm72100OrxccY7Q5XJyTkrLhFN8OJ2KS5Fo8thGWnr+RsxPZqTHdlDUmEStjozOGEpnTsJhEW2lICYMlEoqy8iXWSX9fgV5PMM8ceXo3c2VLH42GHjdU15q819ikund6Jd5dmaGfNrct/Bg3EO4YLD0cLRjSpqNKjTVkr2S7tvi2+b6nLteZncupSkRGqwsWMv8Aw4Tn/itkj65pWuv5blU5awtjFMrlVkuOW/SLcvm0vyKrZ/hZXD8q7Rk8zV2uF9beifApm828rorEeGTkYpY3A9eAqea3VfNf7fkbGC3fSjPXttsEzaayUSMkBIACQAGYAAAAAAAEAANVjd38LWk51Kbk27teJUir9cqaRXOKkzvS2M94jW3twmEp0o5KUI049IpL3fVmcREeFczM+Wj+IOIjT2Vj3LhLDzgv5qn9mvnJF2GN3hVlt00mX5shG8kjq1ju5lp1D2cy5rrYL5GcMJeiMLlkRtVM6Z0/uviTHwxt8wxyjSYljwZiy8wv2dsypiqio05Qg831qjkoxT0V7JvmafMzRipuW7w8M5b6de3W3WpYCh4UJtzk81aqorNVn3bvaPRJaerbfnMnJteXoceCtYbmFCEXdRWb70rzl/mldlE2mV0ViGbZilW4mOmWxKxOkFwIAKbWsfrLVeq5E1t0ztFo3Gm2w1eNSEZx4SV127PudCs7jcNG0anUrkyUJTJEgSBIACwAAABAEoAAAIAgCAPhvjFiMuzHD+9rU4+yvP8A+UbXEru7U5dtUiPu4XRilrzOnXs515mey+GpZCuXsoxsrF9Y017zuU2yvsNaR5hnOF9V7EzG0ROuyb3XdcQjwqmjGVlV+wsR4eKh0mre/wDykc71CnVjn7On6ffpyQ7jgcR4lKE/vRV/Xg/meXns9HC5gQEoZAhgQBDAi4Sz2NUy1KtHlpUh2UtJL8TZ49vMNfkV7RZuEzZazJMkZJgSBIEgWAAAAIQEgACAIAgCANDvrsJY/BVKKt4qtOi3p/axvZejTcfcuwZfp3ifZTnx/UppwP6K4twnFqUW1KMlZxknZprqd+kRMbcC9piV9KjHoi2KwoteSpOK+y37EzMfCaxM+6tTvyZjtlpNOVtCYRMe6Zp8ef5kSRMeEXT9/k+hCdaePEScJRmuMZJr+vWxr569VdNvj21O3ZtzMaqlDLfhaS9JI8lmr02eqx23Xb6AqWIIEXAi4GNwkbIFGIxUIK85RiuraQHp2PUVR+LGLy5XGM3pmV1ey420NrBWY3MtbPaPDbpmy12SYGaZIkCQAFoAAAABAEoAAQBAGIEMgfL747EwVSlUrVcNTnWdlCac6Tc3onOcGm4rWT4+WLLsebJTtWVN8OO3eYfnzCYmb/6r/wAq1XpxOhh5Ez2tbTQzcasd6122+Grz5uE12eVnSpe3zEuXkpWPmHqUoPmk/VF26yp1ZhPDp/aE1iUxeY9hQktJarqiNTCdxPeFVWFteXP9zCYZVtt5MTG6a7FV43DYxzqX23w02lZQi3wbpy99Y/mjzHOpq8vTcK+8cOmHPbqGBi2B5q2JjF2b1fBc36LiyIiZ8JmYjy82JxdWMJSp0JzsuF0m/bj8jOMN2H1K/L4jbG39qTm6dKCo62aVOU5r8eD9jKKRHmGU/aWv2bsXGVsTSjiZ1pylJfxG1Zc5ZOGnoZ63OtI7Vje3ZcNTjCEYRVoxSS9EbURrs0Znc7eiLJQsTAzTAm5Im4E3AuCAJAAAIQEgEAQwIAhgYsgc8+M+Nq0cJQcJJQnVnCdrqTcoOyTXJxVRPtJrmWY43LC86hxHIm/K7P7rdmvR8y5UtVacXZ6+ujt68/mZVvav5ZY3x1v+aHqhXpRy50pSlG7Ulqm29L/7JG1j5evz121cvEmY/BbS+GKoN2tUV+Ci1L8mzZjmYJ+Yas8PkR8SyeIpcvFt1zL8rmU8rD8yxjiZveIV/Sl5ss75YuTu09L25c+xTbm0jxuVteDe35tQ1+I2lf6qb72t8jXvy728dm1j4dK+e7Z7jY+UMRODf10pR/mjx+T+Ry+REz3dPjzEdncqO0qcqcZ5k20rpeZp21WVamh0zvw3dwqqY+pL+HSsvvVZZF7RV5ezSM4w2nywnLWPCiVKpP8AiVpNfdpf2K/FPP8A+xdXDWFU5bSuw9KEFaEVHrZcX1b5vuyyI0rmdvTCRKHohIkXRkELoskWxYQtTAyTAyTJGVwFwLwgCQAAABCAkAhgQwMWBDA5l8dW/oeEXL6S230apyiv9TLMXmVeTw4vF9dez/Rlyp6qHNu+RX8s9b+jMbMoU58zk3zemvJaLS3YRtM6RHLf+l+Tf6Cdkae3au0qNV3hhqFNZFFWjJcLrNeCSb/ZFFMc18zK614t4iGsw3F20vFp26et+3QtlUylDLdWvZ8Xrf24Ex3hE9nu3WnOO0MFNaP6TRXtKSi/lJkWjsms93e2ay9jcBchLJMlCyDA9EGBdBkoXwZItiwLYsIZpgZJkjK4C4HpCAAACQABAEAGBAGLAxYHLvjnictLBRTs3Ou/WKUE7/iizHG9q7zpx/6S19im/wDx/Qs0w39mLxU2002muFm429GuA0bVqq1y+ZIzpVLtft0/4IFamk5t6u1l6XX7ET5ZQiGJa4RTumtW7WfoxPdEdmfiuSV/K1zte47x4O0vduzTX0/BZpt//qw9klbXxI2MbTOkxrbvbNdexYAhKUELIsC6DJF8GShfBgXRZIsiwhYmBkmSJuAuB//Z"
        ),
        DeliveryGuy(
            first_name="Lucas", second_name="Young", address="1818 River Street", city="Nairobi",
            state="Kenya", phone_number="+254701234587", mode="Bike",
            live_location="-1.3140, 36.8360", profile_picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_ff0t2qwKodZd9BiKdhJTCn8PgUEJAhfXsNet9cSbrxFN4RPS--qps1ljeg&s"
        ),
        DeliveryGuy(
            first_name="Charlotte", second_name="Allen", address="1919 Hill Street", city="Nairobi",
            state="Kenya", phone_number="+254701234588", mode="Car",
            live_location="-1.3150, 36.8370", profile_picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRC04cPpQBVPfx4TDlAm0hsnzOEY5bpJG9UNw&s"
        ),
        DeliveryGuy(
            first_name="Benjamin", second_name="King", address="2020 Mountain Street", city="Nairobi",
            state="Kenya", phone_number="+254701234589", mode="Bike",
            live_location="-1.3160, 36.8380", profile_picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGrZT33I05D-IKK8HO-X0jKSqttT3a786GW7ZozrO_WHnDMPSdT0ZLS-X9cQ&s"
        ),
        DeliveryGuy(
            first_name="Amelia", second_name="Scott", address="2121 Valley Street", city="Nairobi",
            state="Kenya", phone_number="+254701234590", mode="Car",
            live_location="-1.3170, 36.8390", profile_picture="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQemseRxpBq2huXEYfXRpA4fCQ6G80ImTGZGA&s"
        ),
    ]

    db.session.add_all(delivery_guys)
    db.session.commit()

