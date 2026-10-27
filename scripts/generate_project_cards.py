#!/usr/bin/env python3
"""Regenerate the four typographic project cards. Requires Pillow, not used by the site build."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--serif',default='/System/Library/Fonts/Supplemental/Georgia.ttf')
    parser.add_argument('--sans',default='/System/Library/Fonts/Supplemental/Arial.ttf')
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    cards=[
        ('projects','Projects','Photography, video, health and sales.','Tools shaped by everyday work.'),
        ('bronze-art-galleries','Bronze Art\nGalleries','Photo delivery built around a photographer’s workflow.','Client delivery · Album selections · Web application'),
        ('cutline','Cutline','Local video clipping for Mac.','Transcription · Vertical framing · Editable captions'),
        ('vitachart','VitaChart','A fertility diary built from family experience.','In development · Private testing'),
    ]
    for slug,title,subtitle,detail in cards:
        img=Image.new('RGB',(1200,630),'#FBFAF7')
        draw=ImageDraw.Draw(img)
        sans=ImageFont.truetype(args.sans,26)
        small=ImageFont.truetype(args.sans,22)
        serif=ImageFont.truetype(args.serif,90 if '\n' in title else 104)
        sub=ImageFont.truetype(args.serif,30)
        draw.text((80,52),'DIOGO SILVA',font=sans,fill='#56534C')
        draw.line((80,112,1120,112),fill='#CEC8BD',width=1)
        draw.multiline_text((76,166),title,font=serif,fill='#191814',spacing=4)
        draw.line((80,391,144,391),fill='#8A6A3C',width=3)
        assert draw.textbbox((0,0),subtitle,font=sub)[2]<=1040
        draw.text((80,418),subtitle,font=sub,fill='#56534C')
        draw.text((80,482),detail,font=small,fill='#746E63')
        draw.text((80,560),'DIOGOBRONZESILVA.COM',font=small,fill='#746E63')
        img.save(args.output/(slug+'.jpg'),quality=92,optimize=True)
    print('Generated four 1200 × 630 project cards.')

if __name__=='__main__':main()
