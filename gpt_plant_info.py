from steamship import Steamship

from config_gpt import KEY


def get_fun_fact(plant_species):
    pkg = Steamship.use(
        "tess-afanasyeva",
        instance_handle="tess-afanasyeva-cfg1",
        api_key=KEY
    )

    resp = pkg.invoke(
        "generate",
        plant=plant_species
    )
    return resp
