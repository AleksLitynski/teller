
import helper
from random import choice


def room_steps():

    print "English + Named"
    english = helper.fork_core_node("noun")

    named = helper.fork_core_node("type", "named")
    helper.add_property(english, named, "english", english)

    nn = helper.node_named(named, english)


    yield

    print "Room + Player"


    room = nn.named("room")

    player = nn.named("player")
    yield

    print "Chair + Player + knows_of + does + doesn't"
    chair = nn.named("chair")

    know_of = helper.fork_core_node("type", "know_of")
    does = helper.fork_core_node("value", "does")
    doesnt = helper.fork_core_node("value", "doesn't")

    helper.add_property(player, know_of, does, chair)
    yield

    print "table"
    table = nn.named("table")
    helper.add_property(player, know_of, does, table)


    print "materials"
    material = nn.named("material")

    plastic = nn.from_named("plastic", material)
    wood = nn.from_named("wood", material)
    aluminum = nn.from_named("aluminum", material)
    duct_tape = nn.from_named("duct tape", material)
    yield

    print "chair + table get materials << This gets put onto the graph soon"
    made_of = helper.fork_core_node("type", "made_of")
    _is = helper.fork_core_node("value", "is")
    is_not = helper.fork_core_node("value", "is_not")

    helper.add_property(chair, made_of, _is, choice([plastic, wood, aluminum, duct_tape]))
    helper.add_property(table, made_of, _is, choice([plastic, wood, aluminum, duct_tape]))
    yield

    print "Bed + Blanket + has"

    bed = nn.named("bed")
    helper.add_property(player, know_of, does, bed)

    blanket = nn.named("blanket")

    have_a = helper.fork_core_node("type", "have_a")
    helper.add_property(bed, have_a, does, blanket)
    yield

    print "colors + bed sizes"
    colored = helper.fork_core_node("type", "colored")
    rgb_color = nn.named("rgb_color")
    colors = {
              "burgundy":nn.from_named("burgundy", rgb_color),
              "violet":nn.from_named("violet", rgb_color),
              "goldenrod":nn.from_named("goldenrod", rgb_color),
              "fuchsia":nn.from_named("fuchsia", rgb_color),
              "lavender":nn.from_named("lavender", rgb_color),
              "beige":nn.from_named("beige", rgb_color),
              "azure":nn.from_named("azure", rgb_color),
              "chartreuse":nn.from_named("chartreuse", rgb_color),
              "sage":nn.from_named("sage", rgb_color),
              "paisley":nn.from_named("paisley", rgb_color),
              "plaid":nn.from_named("plaid", rgb_color),
              "tartan":nn.from_named("tartan", rgb_color),
              "scarlet":nn.from_named("scarlet", rgb_color)
              }

    helper.add_property(blanket, colored, _is, colors[choice(colors.keys())])

    bed_size_type = helper.fork_core_node("type", "bed_size")
    bed_size = nn.named("bed_sizes")
    bed_sizes = {
              "twin":nn.from_named("twin", bed_size),
              "double":nn.from_named("double", bed_size),
              "king":nn.from_named("king", bed_size),
              "queen":nn.from_named("queen", bed_size)
              }
    helper.add_property(bed, bed_size_type, _is, bed_sizes[choice(bed_sizes.keys())])
    yield

    print "floor"

    floor = nn.named("floor")
    helper.add_property(player, know_of, does, floor)

    flooring = nn.from_named("flooring", material)
    floor_material = {
              "hardwood":nn.from_named("hardwood", flooring),
              "linoleum":nn.from_named("linoleum", flooring),
              "concrete":nn.from_named("concrete", flooring),
              "marble":nn.from_named("marble", flooring),
              "carpeted":nn.from_named("carpeted", flooring)
              }

    helper.add_property(floor, made_of, _is, floor_material[choice(floor_material.keys())])

    cup = nn.named("cup")
    helper.add_property(cup, made_of, _is, choice([plastic, wood, aluminum, duct_tape]))
    helper.add_property(table, have_a, does, cup)

    liquid = helper.fork_core_node("noun")
    liquids = {
              "water":nn.from_named("water", liquid),
              "juice":nn.from_named("juice", liquid),
              "wine":nn.from_named("wine", liquid),
              "soda":nn.from_named("soda", liquid),
              "nothing":nn.from_named("nothing", liquid)
              }
    full_of = helper.fork_core_node("type", "full_of")
    helper.add_property(floor, full_of, _is, liquids[choice(liquids.keys())])
    yield



    print "lamp + book"

    lamp = nn.named("lamp")
    helper.add_property(table, have_a, does, lamp)


    book = nn.named("book")
    helper.add_property(table, have_a, does, book)

    titled = helper.fork_core_node("type", "titled")
    title = helper.fork_core_node("noun")
    titles = {
              "Dreams of Potatoes":nn.from_named("Dreams of Potatoes", title),
              "Tequila Sunrise":nn.from_named("Tequila Sunrise", title),
              "The Kraken":nn.from_named("The Kraken", title),
              "40 Cakes":nn.from_named("40 Cakes", title),
              "Spectral Robot Task Force":nn.from_named("Spectral Robot Task Force", title),
              "The Vengeful Penguin":nn.from_named("The Vengeful Penguin", title),
              "Ninja's Guide to Ornamental Horticulture":nn.from_named("Ninja's Guide to Ornamental Horticulture", title),
              "Neko-nomicon":nn.from_named("This is Not a Book", title),
              "40 Cakes":nn.from_named("40 Cakes", title),
              "40 Cakes":nn.from_named("40 Cakes", title)
              }

    helper.add_property(book, titled, _is, titles[choice(titles.keys())])
    yield

    return


def main():
    print "Now Building a room. Press enter to run next step"
    for _ in room_steps():
        raw_input("Press Enter to do next step")

    print "done"


main()
