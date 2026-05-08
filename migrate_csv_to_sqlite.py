from database import force_reimport_all_csv


if __name__ == "__main__":
    force_reimport_all_csv()
    print("CSV component data imported into fld_system_builder.db")