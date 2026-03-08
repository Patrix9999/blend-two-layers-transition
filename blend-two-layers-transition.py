#!/usr/bin/env python3

import sys
import gi

gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gegl', '0.4')

from gi.repository import Gimp, GimpUi, Gtk, Gegl, GObject


class BlendLayersPlugin(Gimp.PlugIn):
    def do_set_i18n(self, procname):
        return False

    def do_query_procedures(self):
        return ["blend-two-layers-transition"]

    def do_create_procedure(self, name):
        proc = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self.run, None)

        proc.set_menu_label("Blend two layers transition")
        proc.add_menu_path("<Image>/Filters/")
        proc.set_documentation(
            "Auto-blends two layers via alpha gradient transition in the middle",
            "Blend two layers transition",
            name,
        )
        proc.set_attribution("Patrix", "Patrix", "2026")

        proc.add_int_argument(
            "blend-percent",
            "Blend percent",
            "Blend size (% of image height)",
            1,
            100,
            20,
            GObject.ParamFlags.READWRITE,
        )

        return proc

    def run(self, procedure, run_mode, image, drawable, args, data):
        GimpUi.init("blend-two-layers-transition.py")

        # Determine blend percent
        blend_percent = args.get_property("blend-percent")

        # Interactive mode using GimpUi.Dialog
        if run_mode == Gimp.RunMode.INTERACTIVE:
            dialog = GimpUi.Dialog(title="Blend two layers", modal=True)

            content_area = dialog.get_content_area()
            content_area.set_spacing(12)

            label = Gtk.Label(label="Blend percent:")
            content_area.add(label)

            scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1)
            scale.set_value(blend_percent)
            scale.set_draw_value(True)
            content_area.add(scale)

            dialog.add_button("_OK", Gtk.ResponseType.OK)
            dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)

            dialog.show_all()
            response = dialog.run()

            if response != Gtk.ResponseType.OK:
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)

            blend_percent = int(scale.get_value())
            args.set_property("blend-percent", blend_percent)
            dialog.destroy()

        # Image dimensions
        width = image.get_width()
        height = image.get_height()

        layers = image.get_layers()
        if len(layers) < 2:
            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)

        top = layers[0]

        # Create gradient mask
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
            y2,
        )

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)


Gimp.main(BlendLayersPlugin.__gtype__, sys.argv)