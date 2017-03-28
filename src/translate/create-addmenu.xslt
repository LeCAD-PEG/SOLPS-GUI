<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <!-- See for serializing content of node: http://stackoverflow.com/questions/13362291/xslcopy-of-just-the-content-without-the-node-->
<xsl:output method="html" />

<xsl:template match="/"># Generated with create-addmenu.xslt
# xsltproc create-addmenu.xslt solps-input.xml > ../../solps-gui/src/widgets/b2menu.py

b2mn_menu = {
# Category : ( parameter, type, default, description )
#         or ( parametergroup, 'paramgroup', [(name, type, default, description)...], description)
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2mn.dat</xsl:with-param>
    <xsl:with-param name="category">Run</xsl:with-param>
  </xsl:call-template> 
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2mn.dat</xsl:with-param>
    <xsl:with-param name="category">Output</xsl:with-param>
  </xsl:call-template> 
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2mn.dat</xsl:with-param>
    <xsl:with-param name="category">Physics</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2mn.dat</xsl:with-param>
    <xsl:with-param name="category">Atomic Physics</xsl:with-param>
  </xsl:call-template> 
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2mn.dat</xsl:with-param>
    <xsl:with-param name="category">Geometry</xsl:with-param>
  </xsl:call-template>    
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2mn.dat</xsl:with-param>
    <xsl:with-param name="category">Atomic Physics</xsl:with-param>
  </xsl:call-template>   
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2ai.dat</xsl:with-param>
    <xsl:with-param name="category">b2ai params</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2ah.dat</xsl:with-param>
    <xsl:with-param name="category">b2ah params</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2ag.dat</xsl:with-param>
    <xsl:with-param name="category">b2ag params</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.neutrals.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.wall_save.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2md.dat</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.boundary.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.feedback_save.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.feedback_control.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.transport.inputfile</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.neutrals_save.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.numerics.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.transport_models_save.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.neutrals.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.transport.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.atomic_physics_rescale.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.user.parameters</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="block">
    <xsl:with-param name="module">b2.parameters</xsl:with-param>
    <xsl:with-param name="category">b2.sources.profile</xsl:with-param>
  </xsl:call-template>

}


</xsl:template>


<xsl:template name="block">
  <xsl:param name = "category" />
  <xsl:param name = "module" />
  '<xsl:value-of select="$category"/>': [ '<xsl:value-of select="b2/module[@name=$module]/@type"/>',
  <xsl:for-each select="b2/module[@name=$module]/category[@name=$category]/switch | b2/module[@name=$module]/category[@name=$category]/switchgroup">
	   <xsl:choose><xsl:when test="name(.)='switchgroup'">
      ( '<xsl:value-of select="name"/>', 'switchgroup', [
        <xsl:for-each select="switch">
               ('<xsl:value-of select="name"/>', '<xsl:value-of select="type"/>', '<xsl:value-of select="default"/>','''<xsl:copy-of select="description/node()"/>'''), 
        </xsl:for-each>],
         """<xsl:copy-of select="description/node()"/>"""),</xsl:when>
      <xsl:otherwise>
         ( '<xsl:value-of select="name"/>', '<xsl:value-of select="type"/>', '<xsl:value-of select="default"/>', """<xsl:copy-of select="description/node()"/>"""),
      </xsl:otherwise>
     </xsl:choose>
   </xsl:for-each>
   ],
</xsl:template>

</xsl:stylesheet>
