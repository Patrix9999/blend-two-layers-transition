#!/usr/bin/env python3

import sys
import gi

gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gegl', '0.4')

from gi.repository import Gimp, GimpUi, Gtk, Gegl

class BlendLayersPlugin(Gimp.PlugIn):
    def do_set_i18n(self, procname):
        return False

    def do_query_procedures(self):
        return ["blend-two-layers-transition"]

    def do_create_procedure(self, name):
        proc = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self.run, None)

        proc.set_menu_label("Blend two layers transition")
        proc.add_menu_path("<Image>/Filters/")
        proc.set_documentation("Auto-blends two layers via alpha gradient transition in the middle", "Blend two layers transition", name)
        proc.set_attribution("Patrix", "Patrix", "2026")

        return proc

    def run(self, procedure, run_mode, image, drawable, args, data):
        if run_mode == Gimp.RunMode.INTERACTIVE:
            blend_percent = 20  # default value
            GimpUi.init("blend-two-layers-transition.py")

            # Popup UI
            dialog = GimpUi.Dialog(
                use_header_bar=False,
                title="Blend two layers transition",
                role="blend-two-layers-transition"
            )

            dialog.add_button("_OK", Gtk.ResponseType.OK)
            dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)

            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            dialog.get_content_area().add(box)
            box.show()

            label = Gtk.Label(label="_Blend size (% of image height, 1-100):")  
            box.pack_start(label, False, False, 0)
            label.show()

            entry = Gtk.Entry()
            entry.set_text(str(blend_percent))
            box.pack_start(entry, False, False, 0)
            entry.show()

            while True:
                response = dialog.run()
                if response == Gtk.ResponseType.OK:
                    try:
                        blend_percent = max(1, min(100, int(entry.get_text())))
                    except ValueError:
                        blend_percent = 20
                    dialog.destroy()
                    break
                else:
                    dialog.destroy()
                    return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)

        width = image.get_width()
        height = image.get_height()

        layers = image.get_layers()
        if len(layers) < 2:
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)

        top = layers[0]

        mask = top.create_mask(Gimp.AddMaskType.WHITE)
        top.add_mask(mask)

        center_y = height / 2
        half_blend = height * (blend_percent / 200.0)

        y1 = max(0, int(round(center_y - half_blend)))
        y2 = min(height, int(round(center_y + half_blend)))

        if y2 <= y1:
            y2 = y1 + 1

        fg = Gegl.Color.new("white")
        bg = Gegl.Color.new("black")

        Gimp.context_set_foreground(fg)
        Gimp.context_set_background(bg)

        mask.edit_gradient_fill(
            Gimp.GradientType.LINEAR,
            0,
            False,
            0,
            0,
            False,
            0,
            y1,
            0,
            y2
        )

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)


Gimp.main(BlendLayersPlugin.__gtype__, sys.argv)