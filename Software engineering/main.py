from filter_class import*

def main():
    from_=input("Enter the flight from:")
    to=input("Enter the flight to:")
    filter_=input("Apply filters:")
    pointer=filters

    if filter_=="Yes":
        rating=input("Enter rating:")
        price=input("Enter price:")
        pointer.search2(to, from_,rating,price)
    elif filter_=="No":
        pointer.search(to, from_)

main()