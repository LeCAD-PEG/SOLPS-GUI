import struct

GE_motion, GE_buttonpress, GE_buttonrelease, GE_keypress, GE_buttonpress_old, \
    GE_buttonrelease_old, GE_keypress_old, GE_modifier, GE_plotdone, \
    GE_replot, GE_reset, GE_fontprops = range(12)

PIPE_IPC = 1
if PIPE_IPC == 1:
    GE_pending = 12
    GE_raise = 13
else:
    GE_raise = 12

GP_BackSpace = 0x08
GP_Tab = 0x09
GP_KP_Enter = 0x0A
GP_Return = 0x0D
GP_Escape = 0x1B
GP_Delete = 127

Mod_Shift = 1
Mod_Ctrl = 1 << 1
Mod_Alt = 1 << 2
Mod_Opt = 1 << 3

GP_FIRST_KEY, GP_Linefeed, GP_Clear, GP_Pause, GP_Scroll_Lock, GP_Sys_Req, \
    GP_Insert, GP_Home, GP_Left, GP_Up, GP_Right, GP_Down, GP_PageUp, \
    GP_PageDown, GP_End, GP_Begin, GP_KP_Space, GP_KP_Tab, GP_KP_F1, GP_KP_F2,\
    GP_KP_F3, GP_KP_F4, GP_KP_Insert, GP_KP_End, GP_KP_Down, GP_KP_Page_Down, \
    GP_KP_Left, GP_KP_Begin, GP_KP_Right, GP_KP_Home, GP_KP_Up, GP_KP_Page_Up,\
    GP_KP_Delete, GP_KP_Equal, GP_KP_Multiply, GP_KP_Add, GP_KP_Separator, \
    GP_KP_Subtract, GP_KP_Decimal, GP_KP_Divide, GP_KP_0, GP_KP_1, GP_KP_2, \
    GP_KP_3, GP_KP_4, GP_KP_5, GP_KP_6, GP_KP_7, GP_KP_8, GP_KP_9, GP_F1, \
    GP_F2, GP_F3, GP_F4, GP_F5, GP_F6, GP_F7, GP_F8, GP_F9, GP_F10, GP_F11, \
    GP_F12, GP_Cancel, GP_Button1, GP_LAST_KEY = range(1000, 1000 + 65)


# The following class are just containers for structs from mousecmn.h. They
# are not really used except for documentation of structs from mousecmn.h.

class gp_event_t(object):
    """ Structure for reporting mouse events to the main program

    Attributes:
        type: Event id
        mx, my: Current mouse coordinates
        par1, par2: Other parameters, depending on type
        winid: ID of window in which the vent occurred

    """
    def __init__(self, type: int, mx: int, my: int, par1: int, par2: int,
                 winid: int) -> None:
        self.type = type
        self.mx = mx
        self.my = my
        self.par1 = par1
        self.par2 = par2
        self.winid = 0  # We do not forward any window id to gnuplot

    def serialize(self) -> bytes:
        return struct.pack("6i", self.type, self.mx, self.my, self.par1,
                           self.par2, self.winid)


class t_gpPMenu(object):
    """Pass information necessary for (un)checking menu items in the
    Presentation Manager terminal.
    Thus this structure is required by pm.trm and gclient.c.
    """

    def __init__(self, use_mouse: int, where_zoom_queue: int,
                 polar_distance: int) -> None:
        self.use_mouse = use_mouse
        self.where_zoom_queue = where_zoom_queue
        self.polar_distance = polar_distance

    def serialize(self) -> bytes:
        return struct.pack("3i", self.use_mouse, self.where_zoom_queue,
                           self.polar_distance)
